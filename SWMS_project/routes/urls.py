from django.urls import path
from .views import route_dashboard
from . import views

urlpatterns = [
    path('dashboard/', route_dashboard, name='route_dashboard'),
    path('optimized-route/', views.get_optimized_route, name='get_optimized_route'),
]
