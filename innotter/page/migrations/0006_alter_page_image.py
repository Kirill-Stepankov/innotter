# Generated by Django 4.2.7 on 2023-11-06 11:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("page", "0005_alter_page_owner"),
    ]

    operations = [
        migrations.AlterField(
            model_name="page",
            name="image",
            field=models.TextField(blank=True, null=True),
        ),
    ]
