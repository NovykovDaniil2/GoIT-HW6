# Generated by Django 4.2.1 on 2023-05-22 19:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("quotes", "0011_rename_authors_quote_author"),
    ]

    operations = [
        migrations.AlterField(
            model_name="author",
            name="biography",
            field=models.CharField(),
        ),
    ]
