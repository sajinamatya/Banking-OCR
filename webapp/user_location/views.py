
from django.shortcuts import render
from django.http import JsonResponse
import requests


def get_location_details(request):
    if request.session.get("user_id") is None:
        return JsonResponse({"error": "User not authenticated"}, status=401)
    latitude = request.GET.get("latitude")
    longitude = request.GET.get("longitude")

    # Debugging: Log the received latitude and longitude values
    print(f"Received latitude: {latitude}, longitude: {longitude}")

    try:
        latitude = float(latitude)
        longitude = float(longitude)
    except (TypeError, ValueError):
        return JsonResponse({"error": "Invalid latitude or longitude"}, status=400)

    if latitude and longitude:
        # Use a Reverse Geocoding API to fetch details
        api_url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={latitude}&lon={longitude}"
        response = requests.get(api_url).json()

        if response:
            location_data = {
                "city": response.get("address", {}).get("city", "Unknown"),
                "district": response.get("address", {}).get("county", "Unknown"),
                "province": response.get("address", {}).get("state", "Unknown"),
                "country": response.get("address", {}).get("country", "Unknown"),
            }
            return JsonResponse(location_data)

    return JsonResponse({"error": "Could not fetch location"}, status=400)


def location_form(request):
    return render(request, "location.html")
