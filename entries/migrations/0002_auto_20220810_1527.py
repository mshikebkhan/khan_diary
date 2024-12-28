# Generated by Django 3.1.6 on 2022-08-10 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entries', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='mood',
            field=models.CharField(choices=[('great', 'Great mood'), ('good', 'Good mood'), ('usual', 'Usual mood'), ('bad', 'Bad mood'), ('terrible', 'Terrible mood')], max_length=30),
        ),
    ]
