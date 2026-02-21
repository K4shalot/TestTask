from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from planner.models import Project, ProjectPlace
from planner.serializers import (
    ProjectCreateUpdateSerializer,
    ProjectPlaceCreateSerializer,
    ProjectPlaceListSerializer,
    ProjectPlaceUpdateSerializer,
    ProjectSerializer,
)


class ProjectViewSet(ModelViewSet):
    """List, create, retrieve, update, delete travel projects."""

    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.prefetch_related("places").order_by("-created_at")

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return ProjectCreateUpdateSerializer
        return ProjectSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        project = serializer.save()
        project = self.get_queryset().get(pk=project.pk)  # prefetch places for response
        return Response(
            ProjectSerializer(project).data,
            status=status.HTTP_201_CREATED,
        )

    def destroy(self, request, *args, **kwargs):
        project = self.get_object()
        if project.places.filter(visited=True).exists():
            return Response(
                {"detail": "Cannot delete project: it has visited places."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProjectPlaceViewSet(ModelViewSet):
    """List, add, retrieve, update places of a project. Nested under /projects/<id>/places/."""

    serializer_class = ProjectPlaceListSerializer
    http_method_names = ["get", "post", "patch", "put", "head", "options"]

    def get_project(self):
        return get_object_or_404(
            Project.objects.prefetch_related("places"),
            pk=self.kwargs["project_pk"],
        )

    def get_queryset(self):
        return ProjectPlace.objects.filter(project_id=self.kwargs["project_pk"]).order_by("id")

    def get_serializer_class(self):
        if self.action == "create":
            return ProjectPlaceCreateSerializer
        if self.action in ("update", "partial_update"):
            return ProjectPlaceUpdateSerializer
        return ProjectPlaceListSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["project"] = self.get_project()
        return context

    def create(self, request, *args, **kwargs):
        project = self.get_project()
        serializer = ProjectPlaceCreateSerializer(
            data=request.data,
            context={"project": project},
        )
        serializer.is_valid(raise_exception=True)
        place = ProjectPlace.objects.create(
            project=project,
            external_artwork_id=serializer.validated_data["external_artwork_id"],
            notes=serializer.validated_data.get("notes") or "",
        )
        return Response(
            ProjectPlaceListSerializer(place).data,
            status=status.HTTP_201_CREATED,
        )
