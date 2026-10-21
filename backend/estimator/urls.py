"""Estimator API endpoints, mounted under /api/ by config.urls."""

from django.urls import path

from . import views

urlpatterns = [
    path("estimate", views.estimate, name="estimate"),
    path("immigration", views.immigration, name="immigration"),
]
