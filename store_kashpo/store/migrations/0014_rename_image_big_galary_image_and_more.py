# Generated by Django 4.2.5 on 2023-11-13 15:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_galary'),
    ]

    operations = [
        migrations.RenameField(
            model_name='galary',
            old_name='image_big',
            new_name='image',
        ),
        migrations.RemoveField(
            model_name='galary',
            name='image_small',
        ),
    ]
