# Generated by Django 4.0 on 2023-11-08 03:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photo', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='photopost',
            old_name='Category',
            new_name='category',
        ),
        migrations.RenameField(
            model_name='photopost',
            old_name='image',
            new_name='image1',
        ),
    ]