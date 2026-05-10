from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('beds/', views.bed_list, name='bed_list'),
    path('beds/<int:pk>/', views.bed_detail, name='bed_detail'),
    path('beds/create/', views.bed_create, name='bed_create'),
    path('beds/<int:pk>/edit/', views.bed_update, name='bed_update'),
    path('beds/<int:pk>/delete/', views.bed_delete, name='bed_delete'),
    path('beds/<int:bed_pk>/plant/', views.plot_create, name='plot_create'),
    path('plots/<int:pk>/edit/', views.plot_update, name='plot_update'),
    path('plots/<int:pk>/delete/', views.plot_delete, name='plot_delete'),
]
