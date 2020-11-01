# Generated by Django 3.0.7 on 2020-10-18 08:01

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import main.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0004_plan_planitem_subscription'),
    ]

    operations = [
        migrations.CreateModel(
            name='Basket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(blank=True, choices=[(10, 'Open'), (20, 'Submitted')], default=10, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            bases=[models.Model],
        ),
        migrations.AlterModelOptions(
            name='plan',
            options={'ordering': ['id']},
        ),
        migrations.AlterField(
            model_name='planitem',
            name='name',
            field=models.CharField(max_length=120, verbose_name='Item name'),
        ),
        migrations.CreateModel(
            name='BasketItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('basket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Basket')),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Plan')),
            ],
            bases=[models.Model],
        ),
    ]