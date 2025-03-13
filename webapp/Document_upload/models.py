from django.db import models
from user_authentication.models import UserAuthentication

class UserDocument(models.Model):
    user = models.OneToOneField(UserAuthentication, on_delete=models.CASCADE, primary_key=True)
    front_side = models.ImageField(upload_to='documents/front_side/')
    back_side = models.ImageField(upload_to='documents/back_side/')
   

    def __str__(self):
        return f"{self.user.username}'s Documents"

    class Meta:
        db_table = 'user_document_detail'
