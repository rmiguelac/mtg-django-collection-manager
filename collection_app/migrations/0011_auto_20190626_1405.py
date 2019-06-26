# Generated by Django 2.2 on 2019-06-26 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collection_app', '0010_auto_20190622_1338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='name',
            field=models.CharField(db_index=True, max_length=128, verbose_name='Card Name'),
        ),
        migrations.AlterField(
            model_name='card',
            name='value',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=6, verbose_name='Value'),
        ),
        migrations.AlterUniqueTogether(
            name='card',
            unique_together={('name', 'set', 'condition', 'foil')},
        ),
    ]
