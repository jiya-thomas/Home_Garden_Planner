from django.urls import path
from . import views

urlpatterns = [
    path('', views.hub, name='agri_hub'),
    path('manage/', views.manage_hub, name='manage_agri_hub'),
    path('add-seed/', views.add_seed, name='add_seed'),
    path('add-fertilizer/', views.add_fertilizer, name='add_fertilizer'),
    path('add-tip/', views.add_tip, name='add_tip'),
]
