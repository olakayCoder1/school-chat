from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.urls import reverse
# Create your models here.

class CustomUser(AbstractUser):
    status = models.BooleanField(default=False)
    address = models.TextField(blank=True)
    profile_image = models.ImageField(default='image-default.png', upload_to='uploads')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class Threads(models.Model):
    CHAT_TYPE = [ 
        ('direct','direct'),
        ('group', 'group')
    ]
    name = models.CharField(max_length=100, unique=True)
    thread_type = models.CharField(max_length=200, choices=CHAT_TYPE )
    created_at = models.DateTimeField(auto_now_add=True)
    discription = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    slug = models.SlugField(null=True)


    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('group_chat', args=[self.name.split('_')[1]])

    



class Messages(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL , null=True)
    thread_name = models.ForeignKey(Threads, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content


