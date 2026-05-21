from django.urls import path
from .views import favorites

urlpatterns = [
    path('', favorites),
]