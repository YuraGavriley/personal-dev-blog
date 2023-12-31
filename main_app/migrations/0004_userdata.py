# Generated by Django 4.2.3 on 2023-09-13 07:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main_app", "0003_alter_comment_options_comment_user_email_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserData",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("username", models.CharField(max_length=65)),
                ("key", models.CharField(max_length=30)),
                ("value", models.CharField(blank=True, max_length=30, null=True)),
            ],
            options={
                "unique_together": {("username", "key")},
            },
        ),
    ]
