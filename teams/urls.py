from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_teams),
    path("save/", views.save_team),
    path("<int:id>/", views.team_detail),

]