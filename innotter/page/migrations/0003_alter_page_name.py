# Generated by Django 4.2.7 on 2023-11-03 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0002_remove_page_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='name',
            field=models.TextField(),
        ),
    ]
