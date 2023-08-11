# Generated by Django 3.1 on 2023-08-10 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='seccion',
            name='form',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='seccion',
            name='description_en',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='seccion',
            name='description_es',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='seccion',
            name='smallDescription_en',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='seccion',
            name='smallDescription_es',
            field=models.TextField(blank=True, null=True),
        ),
    ]