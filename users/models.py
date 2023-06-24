from django.db import models
from django.contrib.auth.models import User

# Create your models here.
GENDER_CHOICES = (
    ('Male','Male'),
    ('Female', 'Female'),
    ('Unknown', 'Prefer not to say'),
    
)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE , null=True)
    fullname = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    email = models.EmailField(unique= True)
    Gender = models.CharField(max_length=7, choices=GENDER_CHOICES, default = 'Male')
    dob = models.DateTimeField(auto_now_add= True)
    Phone = models.IntegerField()
    Address = models.TextField()
    profile_picture = models.ImageField(upload_to = 'profile')
    



    def __str__(self):
        return self.username