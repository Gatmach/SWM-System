from django.db import models
from django.utils import timezone

class WasteBin(models.Model):
    STATUS_CHOICES = [
        ('Empty', 'Empty'),
        ('Partially Full', 'Partially Full'),
        ('Full', 'Full'),
    ]

    location = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Empty')
    fill_level = models.IntegerField(default=0, help_text="Fill percentage (0-100%)")  # New field
    last_updated = models.DateTimeField(default=timezone.now)  # Changed from auto_now

    def __str__(self):
        return f"Bin at {self.location} ({self.status} - {self.fill_level}%)"

    def save(self, *args, **kwargs):
        # Automatically set status based on fill_level when saving
        if self.fill_level <= 20:
            self.status = 'Empty'
        elif self.fill_level <= 80:
            self.status = 'Partially Full'
        else:
            self.status = 'Full'
        
        # Update the last_updated timestamp
        self.last_updated = timezone.now()
        
        super().save(*args, **kwargs)