from django.db import models

# Create your models here.


class ScrapedData(models.Model):
    id = models.IntegerField(blank=True, primary_key=True)
    name = models.CharField(max_length=255)
    website = models.URLField(null=True, blank=True)
    mobile = models.CharField(max_length=20, null=True, blank=True)  # Change to CharField
    address = models.TextField(default='NA')
    query = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
