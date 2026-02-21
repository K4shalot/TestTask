from rest_framework import serializers

from planner.artic_api import artwork_exists
from planner.models import Project, ProjectPlace

MAX_PLACES_PER_PROJECT = 10


class ProjectPlaceListSerializer(serializers.ModelSerializer):
    """Read-only for nested in project."""

    class Meta:
        model = ProjectPlace
        fields = ("id", "external_artwork_id", "notes", "visited", "created_at", "updated_at")
        read_only_fields = fields


class ProjectSerializer(serializers.ModelSerializer):
    places = ProjectPlaceListSerializer(many=True, read_only=True)
    completed = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = (
            "id",
            "name",
            "description",
            "start_date",
            "places",
            "completed",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at", "places", "completed")

    def get_completed(self, obj):
        places = obj.places.all()
        return places.count() > 0 and all(p.visited for p in places)


class ProjectCreateUpdateSerializer(serializers.ModelSerializer):
    """Input: name, description, start_date; optional places (list of external_artwork_id)."""

    places = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        allow_empty=True,
        write_only=True,
    )

    class Meta:
        model = Project
        fields = ("id", "name", "description", "start_date", "places", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")

    def validate_name(self, value):
        if not (value and value.strip()):
            raise serializers.ValidationError("Name is required.")
        return value.strip()

    def validate_places(self, value):
        if not value:
            return []
        ids = [str(x).strip() for x in value if x and str(x).strip()]
        if len(ids) > MAX_PLACES_PER_PROJECT:
            raise serializers.ValidationError(
                f"At most {MAX_PLACES_PER_PROJECT} places per project."
            )
        seen = set()
        for eid in ids:
            if eid in seen:
                raise serializers.ValidationError(
                    f"Duplicate external_artwork_id: {eid!r}."
                )
            seen.add(eid)
            if not artwork_exists(eid):
                raise serializers.ValidationError(
                    f"Artwork {eid!r} not found in Art Institute API."
                )
        return ids

    def create(self, validated_data):
        place_ids = validated_data.pop("places", [])
        project = Project.objects.create(
            name=validated_data["name"],
            description=validated_data.get("description") or "",
            start_date=validated_data.get("start_date"),
        )
        for eid in place_ids:
            ProjectPlace.objects.create(
                project=project,
                external_artwork_id=eid,
                notes="",
            )
        return project


class ProjectPlaceCreateSerializer(serializers.ModelSerializer):
    """Add place to project: external_artwork_id, optional notes."""

    class Meta:
        model = ProjectPlace
        fields = ("external_artwork_id", "notes")

    def validate_external_artwork_id(self, value):
        if not (value and str(value).strip()):
            raise serializers.ValidationError("external_artwork_id is required.")
        value = str(value).strip()
        if not artwork_exists(value):
            raise serializers.ValidationError(
                "Artwork not found in Art Institute API."
            )
        return value

    def validate(self, attrs):
        project = self.context["project"]
        eid = attrs["external_artwork_id"]
        if project.places.filter(external_artwork_id=eid).exists():
            raise serializers.ValidationError(
                {"external_artwork_id": "This place is already in the project."}
            )
        if project.places.count() >= MAX_PLACES_PER_PROJECT:
            raise serializers.ValidationError(
                f"Project may have at most {MAX_PLACES_PER_PROJECT} places."
            )
        return attrs


class ProjectPlaceUpdateSerializer(serializers.ModelSerializer):
    """Update notes and/or visited."""

    class Meta:
        model = ProjectPlace
        fields = ("notes", "visited")
