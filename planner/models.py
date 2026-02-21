from django.db import models


class Project(models.Model):
    """Travel project: name, optional description and start date."""

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    start_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class ProjectPlace(models.Model):
    """Place in a project (Art Institute artwork id), with notes and visited flag."""

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="places",
    )
    external_artwork_id = models.CharField(max_length=100)
    notes = models.TextField(blank=True, default="")
    visited = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["id"]
        constraints = [
            models.UniqueConstraint(
                fields=["project", "external_artwork_id"],
                name="unique_place_per_project",
            )
        ]

    def __str__(self):
        return f"{self.project.name} — place {self.external_artwork_id}"
