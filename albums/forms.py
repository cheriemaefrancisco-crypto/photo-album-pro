from django import forms

from .models import Album, Photo


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ["title", "description"]


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ["album", "title", "caption", "image"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        is_admin = user.is_superuser or user.groups.filter(name="album_admin").exists()
        if not is_admin:
            self.fields["album"].queryset = Album.objects.filter(owner=user)
