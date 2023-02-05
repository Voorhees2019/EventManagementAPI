from config.swagger import swagger_pattern
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    swagger_pattern,
    path("admin/", admin.site.urls),
    path("api/v1/users/", include("apps.users.api.v1.routes")),
]
