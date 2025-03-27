import uuid

from django.db import models

class ImageUpload(models.Model):
    image = models.ImageField(upload_to='uploads/')
    hash = models.CharField(max_length=255, default=uuid.uuid4, unique=True)