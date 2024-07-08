from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class User(AbstractUser):
    userId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="user id")
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=255)
    phone = models.CharField(max_length=255, null=True, blank=True)
   
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'firstName', 'lastName', 'password']
    
    def __str__(self):
        return f"{self.firstName} {self.lastName}, UserID: {self.userId}"
    
    class Meta:
        db_table = 'user'
    
   
class Organisation(models.Model):
    orgId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="org id")
    name = models.CharField(max_length=255)
    description = models.TextField(verbose_name='organisation description', null=True, blank=True)
    users = models.ManyToManyField(User, related_name='organisations')
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'organisation'