import mimetypes
import os

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView as AuthLoginView
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode
from django.views.generic import (CreateView, DeleteView, ListView,
                                  TemplateView, UpdateView)

from .forms import MediaFileRenameForm, MediaFileUploadForm, SignUpForm
from .models import MediaFile, Project, User


class IndexView(LoginRequiredMixin, ListView):
    """ログイン必須のホームページ（プロジェクト一覧）"""

    model = Project
    template_name = "index.html"
    context_object_name = "projects"
    login_url = "app:login"

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user).prefetch_related(
            "media_files"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "title": "Django TailwindCSS Multimedia Auth",
            }
        )
        return context


class LoginView(AuthLoginView):
    """カスタムログインビュー"""

    template_name = "auth/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("app:index")


class SignUpView(CreateView):
    """サインアップビュー"""

    form_class = SignUpForm
    template_name = "auth/signup.html"
    success_url = reverse_lazy("app:signup_done")

    def form_valid(self, form):
        user = form.save()  # メール送信も含む
        # ログインはしない（アクティベーションが必要）
        return redirect(self.success_url)


class SignUpDoneView(TemplateView):
    """サインアップ完了ビュー"""

    template_name = "auth/signup_done.html"


def logout_view(request):
    """カスタムログアウトビュー"""
    logout(request)
    return redirect("app:login")


def activate_user(uidb64, token):
    """ユーザーアクティベーション関数"""
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except Exception:
        return False

    if default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return True
    return False


class ActivateView(TemplateView):
    """アクティベーションビュー"""

    template_name = "auth/activate.html"

    def get(self, request, uidb64, token, *args, **kwargs):
        result = activate_user(uidb64, token)
        context = self.get_context_data(result=result)
        return self.render_to_response(context)


def protected_media(request, path):
    """保護されたメディアファイルへのアクセス制御"""
    user_authenticated = request.user.is_authenticated

    # ログイン済みユーザーは許可
    if user_authenticated:
        pass
    else:
        # 未認証ユーザーはログインページにリダイレクト
        from django.contrib.auth.views import redirect_to_login

        return redirect_to_login(request.get_full_path())

    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if not os.path.exists(file_path):
        raise Http404()

    response = HttpResponse()
    content_type, _ = mimetypes.guess_type(file_path)
    if content_type:
        response["Content-Type"] = content_type
    response["X-Accel-Redirect"] = f"/protected_media/{path}"
    return response


class MediaFileDetailView(LoginRequiredMixin, TemplateView):
    """メディアファイル詳細ビュー"""

    template_name = "multimedia/detail.html"
    login_url = "app:login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        media_file = MediaFile.objects.select_related("project", "user").get(
            pk=kwargs["pk"]
        )

        # ユーザーが所有するファイルかチェック
        if media_file.user != self.request.user:
            raise Http404("ファイルが見つかりません。")

        context["media_file"] = media_file
        context["project"] = media_file.project
        return context


class MediaFileDeleteView(LoginRequiredMixin, DeleteView):
    """メディアファイル削除ビュー"""

    model = MediaFile
    template_name = "multimedia/delete.html"
    success_url = reverse_lazy("app:media_list")
    login_url = "app:login"

    def get_queryset(self):
        # ユーザーが所有するファイルのみ削除可能
        return MediaFile.objects.filter(user=self.request.user).select_related(
            "project", "user"
        )

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        messages.success(self.request, "ファイルを削除しました。")
        project = getattr(self.object, "project", None)
        if project:
            return reverse_lazy(
                "app:project_media_list", kwargs={"project_id": project.id}
            )
        return reverse_lazy("app:project_list")


class MediaFileRenameView(LoginRequiredMixin, UpdateView):
    """メディアファイル名変更ビュー"""

    model = MediaFile
    form_class = MediaFileRenameForm
    template_name = "multimedia/rename.html"
    login_url = "app:login"

    def get_queryset(self):
        # ユーザーが所有するファイルのみ変更可能
        return MediaFile.objects.filter(user=self.request.user).select_related(
            "project", "user"
        )

    def get_success_url(self):
        messages.success(self.request, "ファイル名が正常に変更されました。")
        return reverse_lazy("app:media_detail", kwargs={"pk": self.object.pk})


class ProjectCreateView(LoginRequiredMixin, CreateView):
    """プロジェクト作成"""

    model = Project
    fields = ["name", "description"]
    template_name = "projects/create.html"
    success_url = reverse_lazy("app:index")
    login_url = "app:login"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    """プロジェクト削除"""

    model = Project
    template_name = "projects/delete.html"
    success_url = reverse_lazy("app:index")
    login_url = "app:login"

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user).prefetch_related(
            "media_files"
        )

    def delete(self, request, *args, **kwargs):
        """プロジェクト削除時にメディアファイルも削除"""
        project = self.get_object()
        project_name = project.name
        media_count = project.media_files.count()

        # メディアファイルのレコードを削除（シグナルで物理ファイルも削除される）
        project.media_files.all().delete()

        # プロジェクトを削除
        messages.success(
            request,
            f"プロジェクト「{project_name}」とその中のメディアファイル{media_count}件を削除しました。",
        )
        return super().delete(request, *args, **kwargs)


class ProjectMediaFileListView(LoginRequiredMixin, ListView):
    """特定プロジェクトのメディアファイル一覧"""

    model = MediaFile
    template_name = "multimedia/list.html"
    context_object_name = "media_files"
    paginate_by = 10
    login_url = "app:login"

    def _get_project(self):
        if not hasattr(self, "_project_cache"):
            project_id = self.kwargs.get("project_id")
            try:
                self._project_cache = Project.objects.select_related("owner").get(
                    id=project_id, owner=self.request.user
                )
            except Project.DoesNotExist:
                raise Http404("プロジェクトが見つかりません。")
        return self._project_cache

    def get_queryset(self):
        project = self._get_project()
        return MediaFile.objects.filter(
            user=self.request.user, project=project
        ).select_related("project", "user")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self._get_project()
        context["current_project_id"] = str(project.id)
        context["current_project"] = project
        context["hide_project_filter"] = True
        return context


class ProjectMediaFileUploadView(LoginRequiredMixin, CreateView):
    """特定プロジェクトに対するメディアファイルアップロード"""

    model = MediaFile
    form_class = MediaFileUploadForm
    template_name = "multimedia/upload.html"
    login_url = "app:login"

    def _get_project(self):
        project_id = self.kwargs.get("project_id")
        try:
            return Project.objects.select_related("owner").get(
                id=project_id, owner=self.request.user
            )
        except Project.DoesNotExist:
            raise Http404("プロジェクトが見つかりません。")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        project = self._get_project()
        initial["project"] = project
        return initial

    def form_valid(self, form):
        project = self._get_project()
        form.instance.user = self.request.user
        form.instance.project = project
        form.instance.file_size = form.instance.file.size
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, "ファイルが正常にアップロードされました。")
        return reverse_lazy(
            "app:project_media_list",
            kwargs={"project_id": self.kwargs.get("project_id")},
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["fixed_project"] = self._get_project()
        return context
