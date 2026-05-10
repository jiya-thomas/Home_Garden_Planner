from django.urls import path
from . import views

urlpatterns = [
    path('', views.schedule_list, name='schedule_list'),
    path('add/', views.schedule_create, name='schedule_create'),
    path('<int:pk>/edit/', views.schedule_update, name='schedule_update'),
    path('<int:pk>/done/', views.schedule_done, name='schedule_done'),
    path('<int:pk>/delete/', views.schedule_delete, name='schedule_delete'),
]
