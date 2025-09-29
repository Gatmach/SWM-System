
from django.urls import path
from .views import route_dashboard_view, OptimizeRouteView
from . import views
    
urlpatterns = [
    path("dashboard/", views.route_dashboard_view, name="route_dashboard"),
    path("optimize/", views.OptimizeRouteView.as_view(), name="optimize_route"),
]
