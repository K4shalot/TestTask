from django.urls import include, path
from django.views.generic import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter

from planner.views import ProjectPlaceViewSet, ProjectViewSet

router = DefaultRouter()
router.register(r"projects", ProjectViewSet, basename="project")

places_list = ProjectPlaceViewSet.as_view({"get": "list", "post": "create"})
places_detail = ProjectPlaceViewSet.as_view(
    {"get": "retrieve", "patch": "partial_update", "put": "update"}
)

urlpatterns = [
    path("", RedirectView.as_view(url="/api/", permanent=False)),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path(
        "api/projects/<int:project_pk>/places/",
        places_list,
        name="projectplace-list",
    ),
    path(
        "api/projects/<int:project_pk>/places/<int:pk>/",
        places_detail,
        name="projectplace-detail",
    ),
    path("api/", include(router.urls)),
]
