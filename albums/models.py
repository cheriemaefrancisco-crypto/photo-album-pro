from django.contrib.auth.models import User
from django.db import models
from cloudinary.models import CloudinaryField


class Album(models.Model):
    title = models.CharField(max_length=180)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="albums")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return self.title


class Photo(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name="photos")
    title = models.CharField(max_length=180)
    caption = models.TextField(blank=True)
    image = CloudinaryField("image", folder="photo-album")
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="photos")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.album.title} - {self.title}"
