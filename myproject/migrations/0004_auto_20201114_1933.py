# Generated by Django 3.1.3 on 2020-11-14 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myproject', '0003_auto_20201114_1852'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='artist',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='entry',
            name='title',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]