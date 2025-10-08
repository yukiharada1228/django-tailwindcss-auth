from django.urls import path

from . import views
from .constants import ACCOUNTS_PREFIX

app_name = "app"

urlpatterns = [
    # 認証関連
    path("", views.IndexView.as_view(), name="index"),
    path(f"{ACCOUNTS_PREFIX}login/", views.LoginView.as_view(), name="login"),
    path(f"{ACCOUNTS_PREFIX}logout/", views.logout_view, name="logout"),
    path(f"{ACCOUNTS_PREFIX}signup/", views.SignUpView.as_view(), name="signup"),
    path(
        f"{ACCOUNTS_PREFIX}signup_done/",
        views.SignUpDoneView.as_view(),
        name="signup_done",
    ),
    path(
        f"{ACCOUNTS_PREFIX}activate/<uidb64>/<token>/",
        views.ActivateView.as_view(),
        name="activate",
    ),
    # メディアファイル保護
    path("media/<path:path>", views.protected_media, name="protected_media"),
    # プロジェクト関連
    path("projects/create/", views.ProjectCreateView.as_view(), name="project_create"),
    path(
        "projects/<int:pk>/delete/",
        views.ProjectDeleteView.as_view(),
        name="project_delete",
    ),
    # プロジェクト内メディアファイル関連
    path(
        "projects/<int:project_id>/media/",
        views.ProjectMediaFileListView.as_view(),
        name="project_media_list",
    ),
    path(
        "projects/<int:project_id>/media/upload/",
        views.ProjectMediaFileUploadView.as_view(),
        name="project_media_upload",
    ),
    path(
        "projects/<int:project_id>/media/<int:pk>/",
        views.MediaFileDetailView.as_view(),
        name="media_detail",
    ),
    path(
        "projects/<int:project_id>/media/<int:pk>/delete/",
        views.MediaFileDeleteView.as_view(),
        name="media_delete",
    ),
    path(
        "projects/<int:project_id>/media/<int:pk>/rename/",
        views.MediaFileRenameView.as_view(),
        name="media_rename",
    ),
]
