from rest_framework import serializers

from planner.models import Project, ProjectPlace


class ProjectPlaceListSerializer(serializers.ModelSerializer):
    """Read-only for nested in project."""

    class Meta:
        model = ProjectPlace
        fields = ("id", "external_artwork_id", "notes", "visited", "created_at", "updated_at")
        read_only_fields = fields


class ProjectSerializer(serializers.ModelSerializer):
    places = ProjectPlaceListSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ("id", "name", "description", "start_date", "places", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at", "places")


class ProjectCreateUpdateSerializer(serializers.ModelSerializer):
    """Input: name, description, start_date. Response includes id, created_at, updated_at."""

    class Meta:
        model = Project
        fields = ("id", "name", "description", "start_date", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")

    def validate_name(self, value):
        if not (value and value.strip()):
            raise serializers.ValidationError("Name is required.")
        return value.strip()
