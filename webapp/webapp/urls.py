"""
URL configuration for webapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from user_authentication.views import register_user,verify_email,login_user,send_reset_email,reset_password,logout_user
from user_location.views import get_location_details
from Document_upload.views import document_upload
urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register_user,name='register'),
    path('login/', login_user, name='login'),
    path("document/", document_upload, name="document"),
    path("get-location-details/", get_location_details, name="get_location_details"),
    path('logout/', logout_user, name='logout'),
    path("", login_user),
    path('verify-email/<uidb64>/<token>/',verify_email, name='verify_email'),
    path("send-password-reset/", send_reset_email, name="send-password-reset"),
    path("reset-password/<str:token>/", reset_password, name="reset-password")
    
   
]