# Generated by Django 4.2.5 on 2023-12-12 17:25

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("blogpages", "0011_author_locked_author_locked_at_author_locked_by"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="author",
            options={"permissions": [("can_edit_author_name", "Can edit author name")]},
        ),
    ]