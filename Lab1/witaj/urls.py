from django.urls import path
from . import views

urlpatterns = [
    path(
        "hello_template/<str:name>/",
        views.hello_template,
        name="hello_template"
    ),
    path("time/", views.time, name="time"),
]
