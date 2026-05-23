from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Permission
from django.db.models import Count
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView

from .forms import AlbumForm, PhotoForm
from .models import Album, Photo


class HomeView(TemplateView):
    template_name = "albums/home.html"


def grant_standard_permissions(user):
    if not user.is_authenticated or user.is_superuser:
        return
    codenames = [
        "view_album",
        "add_album",
        "change_album",
        "delete_album",
        "view_photo",
        "add_photo",
        "change_photo",
        "delete_photo",
    ]
    perms = Permission.objects.filter(codename__in=codenames)
    user.user_permissions.add(*perms)


class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        response = super().form_valid(form)
        grant_standard_permissions(self.object)
        messages.success(self.request, "Registration successful. Please log in.")
        return response


class OwnerAdminMixin(LoginRequiredMixin):
    def is_admin(self):
        user = self.request.user
        return user.is_superuser or user.groups.filter(name="album_admin").exists()

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and not self.is_admin():
            grant_standard_permissions(request.user)
        return super().dispatch(request, *args, **kwargs)


class FormTitleMixin:
    model_label = "Item"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = f"Edit {self.model_label}" if getattr(self, "object", None) else f"Create {self.model_label}"
        return context


class AlbumListView(OwnerAdminMixin, PermissionRequiredMixin, ListView):
    permission_required = "albums.view_album"
    model = Album
    context_object_name = "albums"
    template_name = "albums/album_list.html"

    def get_queryset(self):
        qs = Album.objects.annotate(photo_count=Count("photos"))
        return qs if self.is_admin() else qs.filter(owner=self.request.user)


class AlbumDetailView(OwnerAdminMixin, PermissionRequiredMixin, DetailView):
    permission_required = "albums.view_album"
    model = Album
    context_object_name = "album"
    template_name = "albums/album_detail.html"

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if self.is_admin() or obj.owner == request.user:
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseForbidden("You do not have access to this album.")


class AlbumCreateView(FormTitleMixin, OwnerAdminMixin, PermissionRequiredMixin, CreateView):
    permission_required = "albums.add_album"
    model = Album
    model_label = "Album"
    form_class = AlbumForm
    template_name = "albums/form.html"
    success_url = reverse_lazy("albums:album-list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class AlbumUpdateView(FormTitleMixin, OwnerAdminMixin, PermissionRequiredMixin, UpdateView):
    permission_required = "albums.change_album"
    model = Album
    model_label = "Album"
    form_class = AlbumForm
    template_name = "albums/form.html"
    success_url = reverse_lazy("albums:album-list")

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if self.is_admin() or obj.owner == request.user:
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseForbidden("You cannot edit this album.")


class AlbumDeleteView(OwnerAdminMixin, PermissionRequiredMixin, DeleteView):
    permission_required = "albums.delete_album"
    model = Album
    template_name = "albums/confirm_delete.html"
    success_url = reverse_lazy("albums:album-list")

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if self.is_admin() or obj.owner == request.user:
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseForbidden("You cannot delete this album.")


class PhotoCreateView(FormTitleMixin, OwnerAdminMixin, PermissionRequiredMixin, CreateView):
    permission_required = "albums.add_photo"
    model = Photo
    model_label = "Photo"
    form_class = PhotoForm
    template_name = "albums/form.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        album = form.cleaned_data["album"]
        user = self.request.user
        is_admin = user.is_superuser or user.groups.filter(name="album_admin").exists()
        if not is_admin and album.owner != user:
            return HttpResponseForbidden("You can only upload to your own albums.")
        form.instance.uploaded_by = user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("albums:album-detail", kwargs={"pk": self.object.album_id})


class PhotoUpdateView(FormTitleMixin, OwnerAdminMixin, PermissionRequiredMixin, UpdateView):
    permission_required = "albums.change_photo"
    model = Photo
    model_label = "Photo"
    form_class = PhotoForm
    template_name = "albums/form.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if self.is_admin() or obj.uploaded_by == request.user:
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseForbidden("You cannot edit this photo.")

    def get_success_url(self):
        return reverse_lazy("albums:album-detail", kwargs={"pk": self.object.album_id})


class PhotoDeleteView(OwnerAdminMixin, PermissionRequiredMixin, DeleteView):
    permission_required = "albums.delete_photo"
    model = Photo
    template_name = "albums/confirm_delete.html"

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if self.is_admin() or obj.uploaded_by == request.user:
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseForbidden("You cannot delete this photo.")

    def get_success_url(self):
        return reverse_lazy("albums:album-detail", kwargs={"pk": self.object.album_id})
