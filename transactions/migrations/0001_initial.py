# Generated by Django 3.2.2 on 2021-05-11 16:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TransactionCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('income_expense', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Income',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('notes', models.CharField(blank=True, max_length=256, null=True)),
                ('amount', models.FloatField()),
                ('transaction_date', models.DateField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='transactions.transactioncategory')),
            ],
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('notes', models.CharField(blank=True, max_length=256, null=True)),
                ('amount', models.FloatField()),
                ('transaction_date', models.DateField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='transactions.transactioncategory')),
            ],
        ),
    ]
