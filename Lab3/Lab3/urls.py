from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('frontend_demo.urls')),
    path('frontend_demo/', include('frontend_demo.urls')),
    path('', include('tasks.urls')),
    path('tasks/', include('tasks.urls')),
]
