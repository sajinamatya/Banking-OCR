from django.db import models
from django.contrib.auth.hashers import make_password
from django.utils.timezone import now



# Creation of the model for user authenticatin 
class UserAuthentication(models.Model):
    # Primary key of the model 
    user_id = models.AutoField( primary_key=True) 
     # Email of the user 
    email = models.EmailField(max_length=50, unique=True) 
    # password for authentication 
    password = models.CharField(max_length=128)  
    # phone number of the user 
    phone_number = models.CharField(max_length=15, blank=True, null=True)  
    # Account creation date 
    account_created_date = models.DateTimeField(auto_now_add=True) 
    # Email verified status
    is_email_verified = models.BooleanField(default=False) 
    # Login count of the user 
    login_count = models.IntegerField(default=0) 

    last_login = models.DateTimeField(default=now)

    #Defining the custom table name in database for UserAuthentication Model 
    class Meta:
        db_table = 'user_authentication_detail'  

    # Hashing the user password for safety
    def hash_password(password):
        return make_password(password)

    # returns the email of the user
    def get_email_field_name(self):
        return 'email'
