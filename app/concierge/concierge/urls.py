"""concierge URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
import mycore.views as views

static_patterns = static(settings.MEDIA_URL,
                         document_root=settings.MEDIA_ROOT) + \
                  static(settings.STATIC_URL,
                         document_root=settings.STATIC_ROOT)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/<str:model_type>/<int:model_id>', views.model_serialized_view,
         name='api'),
    path('room_create/', views.RoomCreateView.as_view(),
         name='room_create'),
    path('room_search/', views.RoomSearchView.as_view(),
         name='room_search'),
    path('tenant_search/', views.TenantSearchView.as_view(),
         name='tenant_search'),
    path('tenant_create/', views.TenantCreateView.as_view(),
         name='tenant_create'),
    path('room_detailed/', views.RoomDetailView.as_view(),
         name='room_detailed'),
    path('tenant_detailed/', views.TenantDetailView.as_view(),
         name='tenant_detailed'),
    path('success/<str:message>', views.success, name='success'),
    path('journal_search/', views.JournalSearchView.as_view(),
         name='journal_search'),
    path('room_list/', views.RoomListView.as_view(),
         name='room_list'),
    path('tenants_list/', views.TenantListView.as_view(),
         name='tenants_list'),
    path('', views.index, name='index'),
    path('healthcheck/', views.health_check, name='health_check'),
] + static_patterns
