# Generated by Django 4.2.6 on 2023-10-19 01:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0034_alter_comment_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=30),
        ),
    ]
