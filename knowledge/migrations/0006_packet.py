# Generated by Django 2.0.6 on 2019-08-04 14:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hustlers", "0001_initial"),
        ("knowledge", "0005_auto_20180624_1317"),
    ]

    operations = [
        migrations.CreateModel(
            name="Packet",
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
                ("slug", models.CharField(blank=True, max_length=100, null=True)),
                ("sequence_no", models.PositiveIntegerField(default=1)),
                (
                    "created_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="packet",
                        to="hustlers.Hustler",
                    ),
                ),
                (
                    "resources",
                    models.ManyToManyField(
                        related_name="packet", to="knowledge.Category"
                    ),
                ),
            ],
            options={"db_table": "packet",},
        ),
    ]
