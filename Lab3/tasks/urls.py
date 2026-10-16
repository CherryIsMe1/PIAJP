from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/tasks/', views.task_list_create, name='task_list_create'),
    path('api/tasks/<int:task_id>/', views.task_detail, name='task_detail'),
]
