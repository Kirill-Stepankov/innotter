# Generated by Django 4.2.7 on 2023-11-09 09:40

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("page", "0007_alter_page_name"),
    ]

    operations = [
        migrations.RenameField(
            model_name="followers",
            old_name="post",
            new_name="page",
        ),
    ]
