"""
URL configuration for the Django project.

This module defines the URL patterns for the Django project, routing requests 
to the appropriate views based on the URL.

Available routes:
- 'admin/': Routes requests to the Django admin site.
- 'api/': Routes requests to the 'task_one' app's URL configurations.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include("task_one.urls"))
]
