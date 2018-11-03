# Generated by Django 2.1.3 on 2018-11-02 19:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Check',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.IntegerField(blank=True, null=True, verbose_name='ID sur Adhésion')),
                ('card_number', models.CharField(max_length=13, verbose_name='Numero carte VA scanné')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='CheckPlace',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Nom')),
                ('is_active', models.BooleanField(default=True, verbose_name='Actif ?')),
            ],
        ),
        migrations.AddField(
            model_name='check',
            name='check_place',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='checks', to='checker.CheckPlace'),
        ),
    ]