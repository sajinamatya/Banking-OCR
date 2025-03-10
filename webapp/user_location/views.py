import requests
from django.shortcuts import render, redirect
from django.http import JsonResponse
from user_authentication.models import UserAuthentication
from .models import UserLocation
from user_authentication.views import login_required

# OpenStreetMap 
NOMINATIM_URL = "https://nominatim.openstreetmap.org/reverse"


def get_location_details(lat, lng):
    """ Fetch city, district, and province from OpenStreetMap Nominatim API. """
    url = f"{NOMINATIM_URL}?lat={lat}&lon={lng}&format=json"
    response = requests.get(url).json()
    
    if response and 'address' in response:
        address = response['address']
        city = address.get('city', None)
        district = address.get('suburb', None)  
        province = address.get('state', None)
        country = address.get('country', None)
        
        return city, district, province, country
    return None, None, None, None

@login_required
def track_location(request):
    """ Fetch user's location details """
    try:
        user_id = request.session.get('user_id')
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
            city, district, province, country = get_location_details(lat, lng)

            if city and district and province:
                if not user_location:
                    user_location = UserLocation(user=user)

                user_location.latitude = lat
                user_location.longitude = lng
                user_location.city = city
                user_location.district = district
                user_location.province = province
                user_location.country = country
                user_location.save()

                return redirect("location_success")  

  
    context = {
        "latitude": user_location.latitude if user_location else "",
        "longitude": user_location.longitude if user_location else "",
        "city": user_location.city if user_location else "",
        "district": user_location.district if user_location else "",
        "province": user_location.province if user_location else "",
        "country": user_location.country if user_location else "",
    }
    return render(request, "location.html", context)
