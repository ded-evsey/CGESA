# Generated by Django 3.0.7 on 2020-06-28 16:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.TextField()),
                ('name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='CurrencyPerDate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateField()),
                ('main', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='main', to='currency.Currency')),
                ('sub', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub', to='currency.Currency')),
            ],
        ),
    ]
