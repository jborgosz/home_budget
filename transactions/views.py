from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from transactions.forms import ExpenseForm, IncomeForm
from transactions.models import Expense, Income

# Create your views here.


class ExpenseCreateView(CreateView):
    template_name = 'form.html'
    form_class = ExpenseForm
    success_url = reverse_lazy('add_expense')


class IncomeCreateView(CreateView):
    template_name = 'form.html'
    form_class = IncomeForm
    success_url = reverse_lazy('add_income')


class ExpensesView(ListView):
    template_name = 'viewing.html'
    model = Expense
    paginate_by = 20


class IncomesView(ListView):
    template_name = 'viewing.html'
    model = Income
    paginate_by = 20
