from django.db import models

from user_authentication.models import UserAuthentication  # Import your custom auth model

class UserLocation(models.Model):
    user = models.OneToOneField(UserAuthentication, on_delete=models.CASCADE, primary_key=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    province = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now=True)
    
    class Meta:
        
        db_table = 'user_location_detail' 
