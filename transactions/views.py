from datetime import datetime as dt
from itertools import chain
from operator import attrgetter
from logging import getLogger
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from transactions.forms import ExpenseForm, IncomeForm
from transactions.models import Expense, Income
from django.db.models import Count, Sum
from django.contrib.auth.mixins import LoginRequiredMixin
import plotly.express as px
import pandas as pd

# Create your views here.
LOGGER = getLogger()


def balance_amount(user):
    expenses = Expense.objects.filter(user_id=user)
    incomes = Income.objects.filter(user_id=user)
    result = 0

    for transaction in incomes:
        result += transaction.amount

    for transaction in expenses:
        result -= transaction.amount

    return result


def index_bar_graph(user):
    # pass
    categories = [x.category.name for x in
                  Expense.objects.filter(user_id=user).filter(transaction_date__day__gte=dt.today().day - 31)]
    amounts = [x.amount for x in
               Expense.objects.filter(user_id=user).filter(transaction_date__day__gte=dt.today().day - 31)]
    if amounts and categories:
        fig = px.bar(categories,
                     x=categories,
                     y=amounts,
                     labels={'x': 'Categories',
                             'y': 'Amounts'},
                     title='Expenses by categories (last 30 days)',
                     )
        graph = fig.to_html(full_html=False, default_height=400)
        return graph

    else:
        return 'No expenses added'


def index_bar_graph_last_month(user):
    # pass
    amounts_last_two_months = Expense.objects.filter(user_id=user).filter(
        transaction_date__month__gte=dt.today().month - 1).values(
        'transaction_date__month').annotate(sum=Sum('amount'))
    months_listed = [x['transaction_date__month'] for x in
                     list(Expense.objects.filter(user_id=user).values('transaction_date__month').annotate(
                         sum=Sum('amount')))]
    if dt.today().month - 1 in months_listed and dt.today().month in months_listed:
        months = [dt.today().month - 1, dt.today().month]
        amounts = [x['sum'] for x in amounts_last_two_months]

        fig = px.bar(months,
                     x=months,
                     y=amounts,
                     labels={'x': 'Months',
                             'y': 'Amounts'},
                     title='Expenses comparison to last month',
                     )
        graph = fig.to_html(full_html=False, default_height=400)
        return graph
    else:
        return 'Nothing to show here - no expenses in current and/or previous month!'


def index_pie_graph(user):
    # pass
    categories = [x.category.name for x in
                  Expense.objects.filter(user_id=user).filter(transaction_date__day__gte=dt.today().day - 31)]
    amounts = [x.amount for x in
               Expense.objects.filter(user_id=user).filter(transaction_date__day__gte=dt.today().day - 31)]
    data = {x.name: x.amount for x in
            Expense.objects.filter(user_id=user).filter(transaction_date__day__gte=dt.today().day - 31)}
    df = pd.DataFrame(data, index=[0])
    if categories and amounts and data:
        fig = px.pie(df, names=categories, values=amounts)
        graph = fig.to_html(full_html=False, default_height=400)
        return graph
    else:
        return ''


def expenses_pie_graph(user):
    # pass
    categories = [x.category.name for x in Expense.objects.filter(user_id=user).all()]
    amounts = [x.amount for x in Expense.objects.filter(user_id=user).all()]
    data = {x.name: x.amount for x in Expense.objects.filter(user_id=user).all()}
    df = pd.DataFrame(data, index=[0])
    if categories and amounts and data:
        fig = px.pie(df, names=categories, values=amounts)
        graph = fig.to_html(full_html=False, default_height=500)
        return graph
    else:
        return 'Nothing to show yet. Start adding expenses.'


class IndexView(ListView):
    template_name = 'index.html'
    extra_context = {'balance': balance_amount,
                     'expenses_graph': index_bar_graph,
                     'expenses_pie': index_pie_graph,
                     'expenses_graph_last_month': index_bar_graph_last_month, }

    def get_queryset(self):
        if self.request.user.is_authenticated:
            expenses = Expense.objects.filter(user_id=self.request.user).filter(
                transaction_date__day__gte=dt.today().day - 31)
            incomes = Income.objects.filter(user_id=self.request.user).filter(
                transaction_date__day__gte=dt.today().day - 31)
            queryset = list(reversed(sorted(chain(expenses, incomes), key=attrgetter('transaction_date'))))
            return queryset

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            current_user = request.user
            self.extra_context['balance'] = balance_amount(current_user)
            self.extra_context['expenses_graph'] = index_bar_graph(current_user)
            self.extra_context['expenses_pie'] = index_pie_graph(current_user)
            self.extra_context['expenses_graph_last_month'] = index_bar_graph_last_month(current_user)
        return super().dispatch(request, *args, **kwargs)


class ExpenseCreateView(LoginRequiredMixin, CreateView):
    template_name = 'form.html'
    form_class = ExpenseForm
    success_url = reverse_lazy('expenses')

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        return super().form_valid(form)


class IncomeCreateView(LoginRequiredMixin, CreateView):
    template_name = 'form.html'
    form_class = IncomeForm
    success_url = reverse_lazy('incomes')

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        return super().form_valid(form)


class ExpensesView(LoginRequiredMixin, ListView):
    template_name = 'viewing.html'
    model = Expense
    paginate_by = 20
    ordering = ['-transaction_date']
    extra_context = {'pie_chart': expenses_pie_graph}

    def get_queryset(self):
        queryset = list(Expense.objects.filter(user_id=self.request.user))
        return queryset

    def dispatch(self, request, *args, **kwargs):
        current_user = request.user
        self.extra_context['pie_chart'] = expenses_pie_graph(current_user)
        return super().dispatch(request, *args, **kwargs)


class IncomesView(LoginRequiredMixin, ListView):
    template_name = 'viewing.html'
    model = Income
    ordering = ['-transaction_date']
    paginate_by = 20

    def get_queryset(self):
        queryset = Income.objects.filter(user_id=self.request.user)
        return queryset


class ExpenseDetailsView(LoginRequiredMixin, DetailView):
    template_name = 'detail.html'
    model = Expense


class IncomeDetailsView(LoginRequiredMixin, DetailView):
    template_name = 'detail.html'
    model = Income


class ExpenseUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'form.html'
    model = Expense
    form_class = ExpenseForm
    success_url = reverse_lazy('expenses')

    def form_invalid(self, form):
        LOGGER.warning('User provided invalid data on update!')
        return super().form_invalid(form)


class IncomeUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'form.html'
    model = Income
    form_class = IncomeForm
    success_url = reverse_lazy('incomes')

    def form_invalid(self, form):
        LOGGER.warning('User provided invalid data on update!')
        return super().form_invalid(form)


class ExpenseDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'confirm_delete.html'
    model = Expense
    success_url = reverse_lazy('expenses')


class IncomeDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'confirm_delete.html'
    model = Income
    success_url = reverse_lazy('incomes')
