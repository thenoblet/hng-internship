"""
URL configuration for the 'task_one' app.

This module defines the URL patterns for the 'task_one' app, routing requests 
to the appropriate view functions defined in the 'views' module.

Available routes:
- 'hello': Routes requests to the 'hello' view function.
"""

from django.urls import path
from . import views


urlpatterns = [
	path('hello', views.hello, name="hello")
]