# Generated by Django 4.2.6 on 2023-10-11 08:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0023_alter_category_top_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='top_product',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='store.product'),
        ),
    ]
