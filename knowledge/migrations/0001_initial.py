# Generated by Django 2.0.6 on 2018-06-10 06:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

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
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=100)),
                ("description", models.TextField(blank=True, null=True)),
                ("slug", models.CharField(max_length=100)),
            ],
            options={"verbose_name_plural": "categories", "db_table": "category",},
        ),
        migrations.CreateModel(
            name="ExpertiseLevel",
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
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=100)),
                ("slug", models.CharField(max_length=100)),
            ],
            options={"db_table": "expertise_level",},
        ),
        migrations.CreateModel(
            name="KnowledgeStore",
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
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=100)),
                ("url", models.URLField(blank=True, null=True)),
                ("description", models.TextField(blank=True, null=True)),
                ("difficulty_sort", models.PositiveIntegerField(default=1)),
                (
                    "categories",
                    models.ManyToManyField(
                        related_name="knowledge_store", to="knowledge.Category"
                    ),
                ),
                (
                    "expertise_level",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="knowledge_store",
                        to="knowledge.ExpertiseLevel",
                    ),
                ),
            ],
            options={"db_table": "knowledge_store",},
        ),
    ]
