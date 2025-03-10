# Generated by Django 5.1.7 on 2025-03-07 14:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Project",
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
                (
                    "name",
                    models.CharField(
                        help_text="Name or identifier for the project (e.g., '123 Main St').",
                        max_length=200,
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        help_text="Optional detailed description about this project.",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Repair",
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
                (
                    "repair_id",
                    models.PositiveIntegerField(
                        help_text="Numeric ID for this repair within the project."
                    ),
                ),
                (
                    "x_coord",
                    models.FloatField(
                        blank=True,
                        help_text="X coordinate of this repair, if applicable.",
                        null=True,
                    ),
                ),
                (
                    "y_coord",
                    models.FloatField(
                        blank=True,
                        help_text="Y coordinate of this repair, if applicable.",
                        null=True,
                    ),
                ),
                (
                    "label",
                    models.CharField(
                        blank=True,
                        help_text="Descriptive label or name for the repair.",
                        max_length=255,
                    ),
                ),
                (
                    "area_sq_ft",
                    models.FloatField(
                        blank=True,
                        help_text="Estimated area in square feet.",
                        null=True,
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        help_text="The project this repair belongs to.",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="repairs",
                        to="photos.project",
                    ),
                ),
            ],
            options={"unique_together": {("project", "repair_id")},},
        ),
        migrations.CreateModel(
            name="Photo",
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
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("survey", "Survey"),
                            ("demo", "Demo"),
                            ("detail", "Detail"),
                            ("context", "Context"),
                        ],
                        help_text="Category describing what stage or type of photo this is.",
                        max_length=50,
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        help_text="The uploaded image file for this repair photo.",
                        upload_to="photos/",
                    ),
                ),
                (
                    "uploaded_at",
                    models.DateTimeField(
                        auto_now_add=True,
                        help_text="Timestamp when this photo was uploaded.",
                    ),
                ),
                (
                    "repair",
                    models.ForeignKey(
                        help_text="The repair this photo is associated with.",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="photos",
                        to="photos.repair",
                    ),
                ),
            ],
        ),
    ]
