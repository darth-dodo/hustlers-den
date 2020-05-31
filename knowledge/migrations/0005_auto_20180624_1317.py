# Generated by Django 2.0.6 on 2018-06-24 07:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hustlers", "0001_initial"),
        ("knowledge", "0004_auto_20180624_1125"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="created_by",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="categories",
                to="hustlers.Hustler",
            ),
        ),
        migrations.AddField(
            model_name="expertiselevel",
            name="created_by",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="expertise_levels",
                to="hustlers.Hustler",
            ),
        ),
        migrations.AddField(
            model_name="knowledgestore",
            name="created_by",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="knowledge_store",
                to="hustlers.Hustler",
            ),
        ),
        migrations.AddField(
            model_name="mediatype",
            name="created_by",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="media_types",
                to="hustlers.Hustler",
            ),
        ),
    ]
