# Generated by Django 4.2.6 on 2023-11-01 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0043_alter_productimage_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=models.ImageField(blank='', default='static/img/No-Image-Placeholder.png', null=True, upload_to='product_img/'),
        ),
    ]
