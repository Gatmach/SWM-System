from django.contrib import admin
from .models import User, WasteBin, Route
from notification.models import Notification

admin.site.register(User)
admin.site.register(WasteBin)
admin.site.register(Notification)

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ("start_point", "end_point", "distance_km", "estimated_time_min", "created_at")
    search_fields = ("start_point", "end_point")
    filter_horizontal = ("bins",)
