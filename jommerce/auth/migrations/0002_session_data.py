# Generated by Django 4.0.5 on 2022-07-26 05:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auth", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="session",
            name="data",
            field=models.JSONField(blank=True, default=dict, verbose_name="data"),
        ),
    ]