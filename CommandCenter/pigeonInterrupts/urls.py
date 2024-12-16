from django.urls import path
from . import views

app_name = 'pigeonInterrupts'
urlpatterns = [
    path('', views.home_view, name='home'),
    path('list/', views.pigeon_interrupt_list_view, name='pigeon_interrupt_list'),
    path('delete/<int:id>/', views.pigeon_interrupt_delete_view, name='pigeon_interrupt_delete'),
]