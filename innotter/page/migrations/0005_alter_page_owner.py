# Generated by Django 4.2.7 on 2023-11-05 07:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("page", "0004_page_owner_group_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="page",
            name="owner",
            field=models.UUIDField(blank=True, null=True),
        ),
    ]
