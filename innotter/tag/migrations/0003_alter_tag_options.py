# Generated by Django 4.2.7 on 2023-11-11 07:01

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("tag", "0002_alter_tag_name"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="tag",
            options={"ordering": ["name"]},
        ),
    ]
