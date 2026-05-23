from django.urls import path

from . import views

app_name = "albums"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("accounts/signup/", views.SignUpView.as_view(), name="signup"),
    path("albums/", views.AlbumListView.as_view(), name="album-list"),
    path("albums/add/", views.AlbumCreateView.as_view(), name="album-add"),
    path("albums/<int:pk>/", views.AlbumDetailView.as_view(), name="album-detail"),
    path("albums/<int:pk>/edit/", views.AlbumUpdateView.as_view(), name="album-edit"),
    path("albums/<int:pk>/delete/", views.AlbumDeleteView.as_view(), name="album-delete"),
    path("photos/add/", views.PhotoCreateView.as_view(), name="photo-add"),
    path("photos/<int:pk>/edit/", views.PhotoUpdateView.as_view(), name="photo-edit"),
    path("photos/<int:pk>/delete/", views.PhotoDeleteView.as_view(), name="photo-delete"),
]
