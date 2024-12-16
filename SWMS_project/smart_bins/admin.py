from django.contrib import admin
from .models import User
from .models import WasteBin, Route
from notification.models import Notification

# Register your models here.

admin.site.register(User)
admin.site.register(WasteBin)
admin.site.register(Notification)
admin.site.register(Route)

