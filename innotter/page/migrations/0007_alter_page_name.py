# Generated by Django 4.2.7 on 2023-11-06 15:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("page", "0006_alter_page_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="page",
            name="name",
            field=models.TextField(unique=True),
        ),
    ]
