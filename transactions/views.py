from itertools import chain
from operator import attrgetter
from logging import getLogger
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView, UpdateView, DeleteView, DetailView
from transactions.forms import ExpenseForm, IncomeForm
from transactions.models import Expense, Income
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

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


class IndexView(ListView):
    template_name = 'index.html'
    extra_context = {'balance': balance_amount}

    def get_queryset(self):
        expenses = Expense.objects.all()
        incomes = Income.objects.all()
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
    paginate_by = 20


class IncomesView(LoginRequiredMixin, ListView):
    template_name = 'viewing.html'
    model = Income
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
