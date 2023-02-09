# Generated by Django 4.1.2 on 2022-11-01 05:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, verbose_name="name")),
                ("slug", models.SlugField(verbose_name="slug")),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="children",
                        to="blog.category",
                        verbose_name="parent",
                    ),
                ),
            ],
            options={
                "verbose_name": "category",
                "verbose_name_plural": "categories",
            },
        ),
        migrations.AddField(
            model_name="post",
            name="category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="blog.category",
                verbose_name="category",
            ),
        ),
        migrations.AddConstraint(
            model_name="category",
            constraint=models.UniqueConstraint(
                fields=("slug", "parent"), name="unique_slugs_under_same_parent"
            ),
        ),
        migrations.AddConstraint(
            model_name="category",
            constraint=models.UniqueConstraint(
                fields=("name", "parent"), name="unique_names_under_same_parent"
            ),
        ),
    ]
