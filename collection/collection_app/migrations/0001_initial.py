# Generated by Django 2.2 on 2019-04-21 23:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cards',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Card Name')),
                ('edition', models.CharField(max_length=64, verbose_name='Edition')),
                ('condition', models.CharField(max_length=2, verbose_name='Condition')),
                ('quantity', models.IntegerField()),
                ('unit_value', models.FloatField(verbose_name='Single card value')),
                ('value', models.FloatField(verbose_name='Whole quantity value')),
                ('location', models.CharField(max_length=128, verbose_name='Position where stored')),
            ],
        ),
    ]
