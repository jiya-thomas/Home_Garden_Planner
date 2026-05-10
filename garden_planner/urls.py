from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views as core_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', core_views.home, name='home'),
    path('about/', core_views.about, name='about'),
    path('accounts/', include('accounts.urls')),
    path('plants/', include('plants.urls')),
    path('gardens/', include('gardens.urls')),
    path('schedules/', include('schedules.urls')),
    path('tasks/', include('tasks.urls')),
    path('journal/', include('journal.urls')),
    path('agri-hub/', include('agri_department.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
