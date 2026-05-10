from django.urls import path
from . import views

urlpatterns = [
    path('', views.journal_list, name='journal_list'),
    path('<int:pk>/', views.journal_detail, name='journal_detail'),
    path('add/', views.journal_create, name='journal_create'),
    path('<int:pk>/edit/', views.journal_update, name='journal_update'),
    path('<int:pk>/delete/', views.journal_delete, name='journal_delete'),
]
