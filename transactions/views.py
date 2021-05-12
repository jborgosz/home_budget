from logging import getLogger
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView, UpdateView, DeleteView, DetailView
from transactions.forms import ExpenseForm, IncomeForm
from transactions.models import Expense, Income

# Create your views here.
LOGGER = getLogger()


class IndexView(TemplateView):
    template_name = 'index.html'


class ExpenseCreateView(CreateView):
    template_name = 'form.html'
    form_class = ExpenseForm
    success_url = reverse_lazy('expenses')


class IncomeCreateView(CreateView):
    template_name = 'form.html'
    form_class = IncomeForm
    success_url = reverse_lazy('incomes')


class ExpensesView(ListView):
    template_name = 'viewing.html'
    model = Expense
    paginate_by = 20


class IncomesView(ListView):
    template_name = 'viewing.html'
    model = Income
    paginate_by = 20


class ExpenseDetailsView(DetailView):
    template_name = 'detail.html'
    model = Expense


class IncomeDetailsView(DetailView):
    template_name = 'detail.html'
    model = Income


class ExpenseUpdateView(UpdateView):
    template_name = 'form.html'
    model = Expense
    form_class = ExpenseForm
    success_url = reverse_lazy('expenses')

    def form_invalid(self, form):
        LOGGER.warning('User provided invalid data on update!')
        return super().form_invalid(form)


class IncomeUpdateView(UpdateView):
    template_name = 'form.html'
    model = Income
    form_class = IncomeForm
    success_url = reverse_lazy('incomes')

    def form_invalid(self, form):
        LOGGER.warning('User provided invalid data on update!')
        return super().form_invalid(form)


class ExpenseDeleteView(DeleteView):
    template_name = 'confirm_delete.html'
    model = Expense
    success_url = reverse_lazy('expenses')


class IncomeDeleteView(DeleteView):
    template_name = 'confirm_delete.html'
    model = Income
    success_url = reverse_lazy('incomes')
