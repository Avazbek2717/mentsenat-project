# Generated by Django 5.1.5 on 2025-02-02 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_remove_sponser_spent_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='sponser',
            name='work_palce',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
