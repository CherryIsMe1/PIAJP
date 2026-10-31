from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("static_demo.urls")),
    path("static_demo/", include("static_demo.urls")),
]
