"""home_budget URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from transactions.views import (ExpenseCreateView,
                                IncomeCreateView,
                                ExpensesView,
                                IncomesView,
                                IndexView,
                                ExpenseDetailsView,
                                IncomeDetailsView,
                                ExpenseUpdateView,
                                IncomeUpdateView,
                                ExpenseDeleteView,
                                IncomeDeleteView
                                )

urlpatterns = [
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('expenses/', ExpensesView.as_view(), name='expenses'),
    path('incomes/', IncomesView.as_view(), name='incomes'),
    path('add-expense/', ExpenseCreateView.as_view(), name='add_expense'),
    path('add-income/', IncomeCreateView.as_view(), name='add_income'),
    path('expenses/<int:pk>/', ExpenseDetailsView.as_view(), name='expense_details'),
    path('incomes/<int:pk>/', IncomeDetailsView.as_view(), name='income_details'),
    path('update-expense/<int:pk>/', ExpenseUpdateView.as_view(), name='update_expense'),
    path('update-income/<int:pk>/', IncomeUpdateView.as_view(), name='update_income'),
    path('delete-expense/<int:pk>/', ExpenseDeleteView.as_view(), name='delete_expense'),
    path('delete-income/<int:pk>/', IncomeDeleteView.as_view(), name='delete_income'),

]
