import re
from datetime import date
from django.core.exceptions import ValidationError
from django.forms import (DateField, ModelForm)
from transactions.models import Expense, Income


class PastDateField(DateField):

    def validate(self, value):
        super().validate(value)
        if value > date.today():
            raise ValidationError('Future dates are not allowed!')


class ExpenseForm(ModelForm):

    class Meta:
        model = Expense
        fields = '__all__'

    transaction_date = PastDateField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean_notes(self):
        if self.cleaned_data['notes']:
            initial = self.cleaned_data['notes']
            sentences = re.sub(r'\s*\.\s*', '.', initial).split('.')
            return '. '.join(sentence.capitalize() for sentence in sentences)


class IncomeForm(ModelForm):

    class Meta:
        model = Income
        fields = '__all__'

    transaction_date = PastDateField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean_notes(self):
        if self.cleaned_data['notes']:
            initial = self.cleaned_data['notes']
            sentences = re.sub(r'\s*\.\s*', '.', initial).split('.')
            return '. '.join(sentence.capitalize() for sentence in sentences)

