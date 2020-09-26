# Generated by Django 3.0.7 on 2020-09-26 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60, verbose_name='Name')),
                ('description', models.CharField(blank=True, max_length=255, null=True, verbose_name='Description')),
                ('site', models.CharField(max_length=60, verbose_name='Site')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('product_code', models.CharField(blank=True, max_length=60, null=True, verbose_name='Product code')),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]