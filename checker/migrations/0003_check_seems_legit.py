# Generated by Django 2.1.3 on 2018-11-03 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checker', '0002_checkplace_legit_delta'),
    ]

    operations = [
        migrations.AddField(
            model_name='check',
            name='seems_legit',
            field=models.BooleanField(default=True, verbose_name='Semble légitime ?'),
        ),
    ]
