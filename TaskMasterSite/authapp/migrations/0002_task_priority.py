# Generated by Django 5.0.2 on 2024-03-06 04:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("authapp", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="task",
            name="priority",
            field=models.CharField(
                choices=[("H", "High"), ("M", "Medium"), ("L", "Low")],
                default="M",
                max_length=1,
            ),
        ),
    ]
