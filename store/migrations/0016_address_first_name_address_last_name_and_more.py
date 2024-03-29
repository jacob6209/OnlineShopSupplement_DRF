# Generated by Django 4.2.5 on 2023-10-02 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0015_address_zip_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='first_name',
            field=models.CharField(default=9179646209, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='address',
            name='last_name',
            field=models.CharField(default=9179646209, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='address',
            name='phone_number',
            field=models.CharField(default=9179646209, max_length=255),
            preserve_default=False,
        ),
    ]
