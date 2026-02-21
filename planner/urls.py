from django.urls import include, path
from django.views.generic import RedirectView
from rest_framework.routers import DefaultRouter

from planner.views import ProjectViewSet

router = DefaultRouter()
router.register(r"projects", ProjectViewSet, basename="project")

urlpatterns = [
    path("", RedirectView.as_view(url="/api/", permanent=False)),
    path("api/", include(router.urls)),
]
