from django.db import models
from bins.models import WasteBin
from routes.models import Route


# User Model
class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.username



