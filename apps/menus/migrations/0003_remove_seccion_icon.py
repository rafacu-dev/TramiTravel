# Generated by Django 3.1 on 2023-03-12 21:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0002_auto_20230305_0029'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='seccion',
            name='icon',
        ),
    ]
