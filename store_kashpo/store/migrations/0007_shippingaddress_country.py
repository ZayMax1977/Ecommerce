# Generated by Django 4.2.5 on 2023-10-08 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_product_digital'),
    ]

    operations = [
        migrations.AddField(
            model_name='shippingaddress',
            name='country',
            field=models.CharField(blank=True, default='Россия', max_length=200),
        ),
    ]