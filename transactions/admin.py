from django.contrib import admin
from transactions.models import TransactionCategory, Expense, Income

# Register your models here.

admin.site.register(TransactionCategory)
admin.site.register(Expense)
admin.site.register(Income)
