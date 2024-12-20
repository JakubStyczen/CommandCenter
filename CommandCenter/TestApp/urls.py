from django.urls import path
from . import views

app_name = "TestApp"
urlpatterns = [
    path("", views.product_list_view, name="home2"),
]
