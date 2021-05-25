from django.contrib.auth.models import User
from django.db.models import Model, CharField, ForeignKey, DO_NOTHING, FloatField, DateField, BooleanField

# Create your models here.


class TransactionCategory(Model):
    name = CharField(max_length=40)

    def __str__(self):
        return f'{self.name}'

    def __repr__(self):
        return f'{self.name}'


class Income(Model):
    name = CharField(max_length=40)
    notes = CharField(max_length=256, blank=True, null=True)
    category = 'Income'
    amount = FloatField()
    transaction_date = DateField()

    def __str__(self):
        return f'{self.transaction_date} -- {self.amount} -- {self.name}'

    def __repr__(self):
        return f'{self.transaction_date} -- {self.amount} -- {self.name}'


class Expense(Model):
    name = CharField(max_length=40)
    notes = CharField(max_length=256, blank=True, null=True)
    category = ForeignKey(TransactionCategory, on_delete=DO_NOTHING)
    amount = FloatField()
    transaction_date = DateField()
    lat = FloatField(null=True, blank=True, default=51)
    lon = FloatField(null=True, blank=True, default=22)
    user = ForeignKey(User, editable=False, on_delete=DO_NOTHING)

    def __str__(self):
        return f'{self.transaction_date} -- {self.amount} -- {self.name}'

    def __repr__(self):
        return f'{self.transaction_date} -- {self.amount} -- {self.name}'
