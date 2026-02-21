from django.contrib import admin

from planner.models import Project, ProjectPlace


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "start_date", "created_at")


@admin.register(ProjectPlace)
class ProjectPlaceAdmin(admin.ModelAdmin):
    list_display = ("project", "external_artwork_id", "visited", "created_at")
    list_filter = ("visited",)
