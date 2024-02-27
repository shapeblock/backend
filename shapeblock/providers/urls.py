from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProviderViewSet.as_view({
        'get': 'list',
        'post': 'create',
    }), name='provider-list'),
    path('<uuid:uuid>/', views.ProviderViewSet.as_view({
        'get': 'retrieve',
        'delete': 'destroy',
    }), name='provider-detail'),
]
