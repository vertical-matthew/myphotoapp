from django.db import models

"""
In this file, we have introduced three models:

1) Project  - Represents a specific project or job site (e.g., '123 Main Street').
2) Repair   - Represents a specific repair within a project, identified by a numeric repair_id.
3) Photo    - Stores uploaded images tied to a particular repair, with a category 
              (Survey, Demo, Detail, or Context).
"""

class Project(models.Model):
    """
    Project model holds the general information about a project/site.
    You can add more fields like address, manager, etc. as needed.
    """
    name = models.CharField(
        max_length=200,
        help_text="Name or identifier for the project (e.g., '123 Main St')."
    )
    description = models.TextField(
        blank=True,
        help_text="Optional detailed description about this project."
    )
    # Potential fields: managers = models.ManyToManyField(User, blank=True, related_name='managed_projects')

    def __str__(self):
        # Return the name as the display string for this model
        return self.name


class Repair(models.Model):
    """
    Repair model belongs to a Project.
    It can store relevant details such as coordinates or area for that repair.
    """
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='repairs',
        help_text="The project this repair belongs to."
    )
    repair_id = models.PositiveIntegerField(
        help_text="Numeric ID for this repair within the project."
    )
    x_coord = models.FloatField(
        null=True,
        blank=True,
        help_text="X coordinate of this repair, if applicable."
    )
    y_coord = models.FloatField(
        null=True,
        blank=True,
        help_text="Y coordinate of this repair, if applicable."
    )
    label = models.CharField(
        max_length=255,
        blank=True,
        help_text="Descriptive label or name for the repair."
    )
    area_sq_ft = models.FloatField(
        null=True,
        blank=True,
        help_text="Estimated area in square feet."
    )

    class Meta:
        # Enforce that a given project cannot have duplicate repair_ids
        unique_together = ('project', 'repair_id')

    def __str__(self):
        return f"Repair {self.repair_id} for {self.project.name}"


class Photo(models.Model):
    """
    Photo model is linked to a specific Repair.
    The category field identifies the stage/type of photo (Survey, Demo, etc.).
    """
    repair = models.ForeignKey(
        Repair,
        on_delete=models.CASCADE,
        related_name='photos',
        help_text="The repair this photo is associated with."
    )
    category = models.CharField(
        max_length=50,
        choices=[
            ('survey', 'Survey'),
            ('demo', 'Demo'),
            ('detail', 'Detail'),
            ('context', 'Context')
        ],
        help_text="Category describing what stage or type of photo this is."
    )
    image = models.ImageField(
        upload_to='photos/',
        help_text="The uploaded image file for this repair photo."
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when this photo was uploaded."
    )

    def __str__(self):
        # Display which category photo this is and which repair it belongs to
        return f"{self.get_category_display()} Photo (Repair {self.repair.repair_id})"
