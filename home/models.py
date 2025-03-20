from django.contrib.auth.models import AbstractUser
from django.db import models



# Create your models here.


class ScrapedData(models.Model):
    id = models.IntegerField(blank=True, primary_key=True)
    session_id = models.CharField(max_length=100,blank=True)
    name = models.CharField(max_length=255)
    website = models.URLField(null=True, blank=True)
    mobile = models.CharField(max_length=20, null=True, blank=True)  # Change to CharField
    address = models.TextField(default='NA')
    query = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
class CustomUser(AbstractUser):
    user_id = models.CharField(max_length=200, unique=True)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Use a unique related_name
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  # Use a unique related_name
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.username