from django.urls import path

from . import views
from .constants import ACCOUNTS_PREFIX

app_name = "app"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path(f"{ACCOUNTS_PREFIX}login/", views.LoginView.as_view(), name="login"),
    path(f"{ACCOUNTS_PREFIX}logout/", views.logout_view, name="logout"),
    path(f"{ACCOUNTS_PREFIX}signup/", views.SignUpView.as_view(), name="signup"),
    path(f"{ACCOUNTS_PREFIX}signup_done/", views.SignUpDoneView.as_view(), name="signup_done"),
    path(
        f"{ACCOUNTS_PREFIX}activate/<uidb64>/<token>/",
        views.ActivateView.as_view(),
        name="activate",
    ),
    path("media/<path:path>", views.protected_media, name="protected_media"),
    # メディアファイル関連
    path("media-files/", views.MediaFileListView.as_view(), name="media_list"),
    path(
        "media-files/upload/", views.MediaFileUploadView.as_view(), name="media_upload"
    ),
    path(
        "media-files/<int:pk>/",
        views.MediaFileDetailView.as_view(),
        name="media_detail",
    ),
    path(
        "media-files/<int:pk>/delete/",
        views.MediaFileDeleteView.as_view(),
        name="media_delete",
    ),
    path(
        "media-files/<int:pk>/rename/",
        views.MediaFileRenameView.as_view(),
        name="media_rename",
    ),
]
