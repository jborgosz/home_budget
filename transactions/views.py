from datetime import datetime as dt
from itertools import chain
from operator import attrgetter
from logging import getLogger
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView, UpdateView, DeleteView, DetailView
from transactions.forms import ExpenseForm, IncomeForm
from transactions.models import Expense, Income
from django.db.models import Count, Sum
from django.contrib.auth.mixins import LoginRequiredMixin
import plotly.express as px
import pandas as pd

# Create your views here.
LOGGER = getLogger()


def balance_amount():
    expenses = Expense.objects.all()
    incomes = Income.objects.all()
    result = 0

    for transaction in incomes:
        result += transaction.amount

    for transaction in expenses:
        result -= transaction.amount

    return result


def index_bar_graph():
    categories = [x.category.name for x in Expense.objects.filter(transaction_date__day__gte=dt.today().day - 31)]
    amounts = [x.amount for x in Expense.objects.filter(transaction_date__day__gte=dt.today().day - 31)]

    fig = px.bar(categories,
                 x=categories,
                 y=amounts,
                 labels={'x': 'Categories',
                         'y': 'Amounts'},
                 title='Expenses by categories (last month)',
                 )
    graph = fig.to_html(full_html=False, default_height=400)
    return graph


def index_bar_graph_last_month():
    amounts_last_two_months = Expense.objects.filter(transaction_date__month__gte=dt.today().month-1).values('transaction_date__month').annotate(sum=Sum('amount'))
    months_listed = [x['transaction_date__month'] for x in list(Expense.objects.values('transaction_date__month').annotate(sum=Sum('amount')))]
    if dt.today().month-1 in months_listed:
        months = [dt.today().month-1, dt.today().month]
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
        return 'Nothing to show here - no expenses in previous month!'


def index_pie_graph():

    categories = [x.category.name for x in Expense.objects.filter(transaction_date__day__gte=dt.today().day - 31)]
    amounts = [x.amount for x in Expense.objects.filter(transaction_date__day__gte=dt.today().day - 31)]
    data = {x.name: x.amount for x in Expense.objects.filter(transaction_date__day__gte=dt.today().day - 31)}
    df = pd.DataFrame(data, index=[0])

    fig = px.pie(df, names=categories, values=amounts)
    graph = fig.to_html(full_html=False, default_height=400)
    return graph


def expenses_pie_graph():

    categories = [x.category.name for x in Expense.objects.all()]
    amounts = [x.amount for x in Expense.objects.all()]
    data = {x.name: x.amount for x in Expense.objects.all()}
    df = pd.DataFrame(data, index=[0])

    fig = px.pie(df, names=categories, values=amounts)
    graph = fig.to_html(full_html=False, default_height=500)
    return graph


class IndexView(ListView):
    template_name = 'index.html'
    extra_context = {'balance': balance_amount,
                     'expenses_graph': index_bar_graph(),
                     'expenses_pie': index_pie_graph(),
                     'expenses_graph_last_month': index_bar_graph_last_month(),}

    def get_queryset(self):
        expenses = Expense.objects.filter(transaction_date__day__gte=dt.today().day - 31)
        incomes = Income.objects.filter(transaction_date__day__gte=dt.today().day - 31)
        queryset = list(reversed(sorted(chain(expenses, incomes), key=attrgetter('transaction_date'))))
        return queryset


class ExpenseCreateView(LoginRequiredMixin, CreateView):
    template_name = 'form.html'
    form_class = ExpenseForm
    success_url = reverse_lazy('expenses')

    def form_valid(self, form):
        cleaned_data = form.cleaned_data

        return super().form_valid(form)


class IncomeCreateView(LoginRequiredMixin, CreateView):
    template_name = 'form.html'
    form_class = IncomeForm
    success_url = reverse_lazy('incomes')


class ExpensesView(LoginRequiredMixin, ListView):
    template_name = 'viewing.html'
    model = Expense
    ordering = ['-transaction_date']
    paginate_by = 20
    extra_context = {'pie_chart': expenses_pie_graph()}


class IncomesView(LoginRequiredMixin, ListView):
    template_name = 'viewing.html'
    model = Income
    ordering = ['-transaction_date']
    paginate_by = 20


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
