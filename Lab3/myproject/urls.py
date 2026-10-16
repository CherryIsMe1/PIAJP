from django.contrib import admin
from django.urls import path, include
from tasks import views as task_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('frontend_demo.urls')),
    path('taskboard/', task_views.index, name='taskboard'),
    path('api/tasks/', task_views.task_list_create, name='task_list_create'),
    path('api/tasks/<int:task_id>/', task_views.task_detail, name='task_detail'),
]
