from django.shortcuts import render,redirect
import requests
from django.http import JsonResponse
from user_authentication.models import UserAuthentication  # Import custom auth model
from .models import UserLocation
from user_authentication.views import login_required
# Google Maps API Key
GOOGLE_MAPS_API_KEY = "YOUR_GOOGLE_MAPS_API_KEY"

@login_required
def get_location_details(request,lat, lng):
    """ Fetch city, district, and province from Google Maps API. """
    url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lng}&key={GOOGLE_MAPS_API_KEY}"
    response = requests.get(url).json()
    
    if response["status"] == "OK":
        address_components = response["results"][0]["address_components"]
        city, district, province, country = None, None, None, None
        
        for component in address_components:
            if "locality" in component["types"]:
                city = component["long_name"]
            elif "administrative_area_level_2" in component["types"]:
                district = component["long_name"]
            elif "administrative_area_level_1" in component["types"]:
                province = component["long_name"]
            elif "country" in component["types"]:
                country = component["long_name"]
        
        return city, district, province, country
    return None, None, None, None

@login_required
def track_location(request, user_id):
    """ Fetch user's location details """
    try:
        user = UserAuthentication.objects.get(pk=user_id)
        user_location = UserLocation.objects.filter(user=user).first()
        return render(request, "location.html", {"user_location": user_location, "user": user})
    except UserAuthentication.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)

@login_required
def update_location(request):
    user = request.session.get('user_id') 
    user_location = UserLocation.objects.filter(user=user).first()

    if request.method == "POST":
        lat = request.POST.get("latitude")
        lng = request.POST.get("longitude")

        if lat and lng:
            city, district, province = get_location_details(lat, lng)

            if city and district and province:
                if not user_location:
                    user_location = UserLocation(user=user)

                user_location.latitude = lat
                user_location.longitude = lng
                user_location.city = city
                user_location.district = district
                user_location.province = province
                user_location.save()

                return redirect("location_success")  # Redirect after saving

    # Pre-fill form with existing data
    context = {
        "latitude": user_location.latitude if user_location else "",
        "longitude": user_location.longitude if user_location else "",
        "city": user_location.city if user_location else "",
        "district": user_location.district if user_location else "",
        "province": user_location.province if user_location else "",
    }
    return render(request, "location.html", context)