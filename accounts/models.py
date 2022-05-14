from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.

Users = get_user_model()

class TokenActivation(models.Model):
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    token = models.CharField(max_length=150)