# Generated by Django 3.2.3 on 2021-05-17 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0002_remove_income_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='lonlat',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]