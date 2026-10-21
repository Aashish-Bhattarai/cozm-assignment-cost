"""URL configuration for the Assignment Cost Estimate API."""

from django.urls import include, path

urlpatterns = [
    path("api/", include("estimator.urls")),
]
