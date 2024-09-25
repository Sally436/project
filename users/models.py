from django.db import models
import geocoder
from geopy.geocoders import Nominatim
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=100, null=True)
    ghana_card = models.CharField(max_length=30, null=True, blank=True)
    phone = models.CharField(max_length=10, null=True)
    image = models.ImageField(default='default.png',upload_to='media')
    latitude = models.FloatField(default=0.0, null=True, blank=True)
    longitude = models.FloatField(default=0.0, null=True, blank=True)
    
    def __str__(self):
        return f'{self.user.username} - Profile'
    
    def save(self, *args, **kwargs):
        if self.address:
            geolocator = Nominatim(user_agent="geoapiExercises")
            location = geolocator.geocode(self.address)
            if location:
                self.latitude = location.latitude
                self.longitude = location.longitude
            else:
                self.latitude = 0.0
                self.longitude = 0.0
        super().save(*args, **kwargs)

class Processor_Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=100, null=True)
    ghana_card = models.CharField(max_length=30, null=True, blank=True)
    phone = models.CharField(max_length=10, null=True)
    FDA_Number = models.CharField(max_length=20, null=True)
    reports = models.FileField(
        upload_to='documents/', 
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png', 'gif'])]
    )
    image = models.ImageField(default='default.png',upload_to='media')

    def __str__(self):
        return f'{self.user.username} - Profile'


