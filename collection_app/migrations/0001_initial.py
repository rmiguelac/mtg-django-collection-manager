# Generated by Django 2.2 on 2019-08-11 23:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=128, verbose_name='Card Name')),
                ('expansion', models.CharField(blank=True, max_length=64, verbose_name='Expansion')),
                ('condition', models.CharField(blank=True, max_length=2, verbose_name='Condition')),
                ('foil', models.BooleanField(default=False, null=True, verbose_name='Foil')),
                ('quantity', models.IntegerField(default=1, verbose_name='Quantity')),
                ('value', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=6, verbose_name='Value')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cards', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('name', 'expansion', 'condition', 'foil')},
            },
        ),
    ]
