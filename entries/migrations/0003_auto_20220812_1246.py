# Generated by Django 3.1.6 on 2022-08-12 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entries', '0002_auto_20220810_1527'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='content',
            field=models.TextField(max_length=750),
        ),
    ]