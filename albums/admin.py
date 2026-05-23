from django.contrib import admin

from .models import Album, Photo


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "updated_at")


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ("title", "album", "uploaded_by", "created_at")
