from django.shortcuts import render 
from django.core.mail import send_mail
from user_authentication.models import UserAuthentication
from django.http import HttpResponse 
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.shortcuts import redirect
from django.core.signing import TimestampSigner, BadSignature, SignatureExpired


def register_user(request) :  
    
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        re_type_password = request.POST.get('re-password')
        phone_number = request.POST.get('phone')
        hashed_password = UserAuthentication.hash_password(password)
        # Checking if the email already exist in the database or not 
        if UserAuthentication.objects.filter(email=email).exists():
            return render(request, "register.html", {"error": "The entered email already exists in the system."})
        
        if UserAuthentication.objects.filter(phone_number=phone_number).exists():
            return render(request, "register.html", {"error": "The entered phone number is  already exists in the system."})
        # Checking if the password field data and re-type password field data matches or not 
        if password != re_type_password:
            return render(request, "register.html", {"error": "Retype password do not match."})
          
        user = UserAuthentication.objects.create(
            email=email,
            password=hashed_password,  
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
        # Checking if the user email is already verified or not 
        if user.is_email_verified:
            return HttpResponse("Your email is already verified.", status=200)
        
        if default_token_generator.check_token(user, token):
            if request.method == "POST":
                user.is_email_verified = True
                user.save()
                return HttpResponse("Email verified successfully! You can now log in.", status=200)

            return render(request, 'emailverification.html', {'email': user.email})

    except (TypeError, ValueError, OverflowError, UserAuthentication.DoesNotExist):
        return HttpResponse("Invalid verification link.", status=400)

    return HttpResponse("Invalid or expired token.", status=400)



def login_user(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = UserAuthentication.objects.get(email=email)
        except UserAuthentication.DoesNotExist:
            return render(request, "login.html", {"error": "Email is invalid!"})


        if user.is_email_verified == 0: 
            return render(request, "login.html", {"error": "Please verify your email before logging in."})

        

        if check_password(password, user.password):
            # Store user ID in session
            
            request.session['user_id'] = user.user_id
            request.session.modified = True  
            request.session.save()
            user.login_count += 1
            print("SESSION DATA:", request.session.items()) 
            user.save()

            return redirect('document')  
        else:
            return render(request, "login.html", {"error": "Password is incorrect!"})

    return render(request, 'login.html')




def logout_user(request):
    request.session.flush()  
    return redirect('login')






signer = TimestampSigner()


def generate_reset_token(user_id):
    return signer.sign(user_id)

# Validate and extract user ID from token
def verify_reset_token(token, max_age=1800):  # 30 minutes expiry
    try:
        user_id = signer.unsign(token, max_age=max_age)  # Returns user ID if valid
        return user_id
    except (BadSignature, SignatureExpired):
        return None  # Invalid or expired token
    
def send_reset_email(request):
    if request.method == "POST":
        email = request.POST.get('email')

        try:
            user = UserAuthentication.objects.get(email=email)

            if not user.is_email_verified:
                return HttpResponse("Email is not verified.", status=400)

            reset_token = generate_reset_token(user.user_id)
            reset_link = f"http://127.0.0.1:8000/reset-password/{reset_token}/"

            send_mail(
                subject="Password Reset Request",
                message=f"Click the link below to reset your password:\n{reset_link}",
                from_email=settings.EMAIL_HOST_USER ,
                recipient_list=[email],
                fail_silently=False,
            )

            return HttpResponse("Please check your email, password reset link has been sent to your email.")
        
        except UserAuthentication.DoesNotExist:
            return HttpResponse("Email not found.", status=400)

    return render(request, "reset.html")

def reset_password(request, token):
    user_id = verify_reset_token(token)

    if not user_id:
        return HttpResponse("Reset link expired or invalid.", status=400)

    if request.method == "POST":
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if new_password != confirm_password:
            return HttpResponse("Passwords do not match.", status=400)


        try:
            user = UserAuthentication.objects.get(user_id=user_id)
            user.password = UserAuthentication.hash_password(new_password) 
            user.save()
            return HttpResponse("Password has been reset successfully.")
        except UserAuthentication.DoesNotExist:
            return HttpResponse("User not found.", status=400)

    return render(request, "password_reset_form.html", {"token": token})