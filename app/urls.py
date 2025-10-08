from django.urls import path

from . import views

app_name = "app"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("accounts/login/", views.LoginView.as_view(), name="login"),
    path("accounts/logout/", views.logout_view, name="logout"),
    path("accounts/signup/", views.SignUpView.as_view(), name="signup"),
    path("accounts/signup_done/", views.SignUpDoneView.as_view(), name="signup_done"),
    path(
        "accounts/activate/<uidb64>/<token>/",
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
