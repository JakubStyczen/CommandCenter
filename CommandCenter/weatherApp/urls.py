from django.urls import path
from . import views

app_name = "weatherApp"
urlpatterns = [
    path("", views.home_view, name="home"),
    path("list/", views.weather_conditions_list_view, name="weather_conditions_list"),
    path(
        "delete/<int:id>/",
        views.weather_conditions_delete_view,
        name="weather_conditions_delete",
    ),
    path(
        "create/",
        views.weather_conditions_create_view,
        name="weather_conditions_create",
    ),
    path(
        "update/<int:id>/",
        views.weather_conditions_update_view,
        name="weather_conditions_update",
    ),
]
