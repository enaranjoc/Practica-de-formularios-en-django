from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Post(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=300)

