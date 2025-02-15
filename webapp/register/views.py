from django.shortcuts import render 
from django.core.mail import send_mail
from register.models import UserAuthentication
from django.http import HttpResponse 
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.urls import reverse
from django.conf import settings


def register_user(request) :  
    
    if request.method == "POST":
        email = request.POST.get('Email')
        password = request.POST.get('Password')
        re_type_password = request.POST.get('Re-type Password')
        phone_number = request.POST.get('phone')

        # Checking if the email already exist in the database or not 
        if UserAuthentication.objects.filter(email=email).exists():
            return HttpResponse("The entered email already exists in the system.", status=400)
        
        if UserAuthentication.objects.filter(phone_number=phone_number).exists():
            return HttpResponse("The entered phone number is  already exists in the system.", status=400)
        # Checking if the password field data and re-type password field data matches or not 
        if password != re_type_password:
            return HttpResponse("Retype password do not match", status=400)
        
        user = UserAuthentication.objects.create(
            email=email,
            password=password,  
            phone_number=phone_number,
            is_email_verified=False
        )
        send_verification_email(request, user)
        return HttpResponse("Verification email sent. Please check your inbox.", status=200)
        # Creation of the UserAuthentication model object 
        
    else:
        return render(request,'register.html')
    

def send_verification_email(request, user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))

    verification_url = request.build_absolute_uri(reverse('verify_email', kwargs={'uidb64': uid, 'token': token}))

    subject = "Sajilo Ebank, Please Verify Your Email"
    message = f"Click the link to verify your email: {verification_url}"
    sender_email = settings.EMAIL_HOST_USER 
    send_mail(subject, message, sender_email, [user.email], fail_silently=False)


def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserAuthentication.objects.get(pk=uid)

        if default_token_generator.check_token(user, token):
            if request.method == "POST":
                user.is_email_verified = True
                user.save()
                return HttpResponse("Email verified successfully! You can now log in.", status=200)

            return render(request, 'emailverification.html', {'email': user.email})

    except (TypeError, ValueError, OverflowError, UserAuthentication.DoesNotExist):
        return HttpResponse("Invalid verification link.", status=400)

    return HttpResponse("Invalid or expired token.", status=400)