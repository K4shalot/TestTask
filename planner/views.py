from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from planner.models import Project
from planner.serializers import ProjectCreateUpdateSerializer, ProjectSerializer


class ProjectViewSet(ModelViewSet):
    """List, create, retrieve, update, delete travel projects."""

    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.prefetch_related("places").order_by("-created_at")

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return ProjectCreateUpdateSerializer
        return ProjectSerializer

    def destroy(self, request, *args, **kwargs):
        project = self.get_object()
        if project.places.filter(visited=True).exists():
            return Response(
                {"detail": "Cannot delete project: it has visited places."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
