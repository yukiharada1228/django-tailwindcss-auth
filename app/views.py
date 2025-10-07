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
from django.views.generic import CreateView, DeleteView, ListView, TemplateView

from .forms import MediaFileUploadForm, SignUpForm
from .models import MediaFile, User


class IndexView(LoginRequiredMixin, TemplateView):
    """ログイン必須のホームページ"""

    template_name = "index.html"
    login_url = "app:login"

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


class MediaFileListView(LoginRequiredMixin, ListView):
    """メディアファイル一覧ビュー"""

    model = MediaFile
    template_name = "multimedia/list.html"
    context_object_name = "media_files"
    paginate_by = 10
    login_url = "app:login"

    def get_queryset(self):
        return MediaFile.objects.filter(user=self.request.user)


class MediaFileUploadView(LoginRequiredMixin, CreateView):
    """メディアファイルアップロードビュー"""

    model = MediaFile
    form_class = MediaFileUploadForm
    template_name = "multimedia/upload.html"
    success_url = reverse_lazy("app:media_list")
    login_url = "app:login"

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.file_size = form.instance.file.size
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, "ファイルが正常にアップロードされました。")
        return super().get_success_url()


class MediaFileDetailView(LoginRequiredMixin, TemplateView):
    """メディアファイル詳細ビュー"""

    template_name = "multimedia/detail.html"
    login_url = "app:login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        media_file = MediaFile.objects.get(pk=kwargs["pk"])

        # ユーザーが所有するファイルかチェック
        if media_file.user != self.request.user:
            raise Http404("ファイルが見つかりません。")

        context["media_file"] = media_file
        return context


class MediaFileDeleteView(LoginRequiredMixin, DeleteView):
    """メディアファイル削除ビュー"""

    model = MediaFile
    template_name = "multimedia/delete.html"
    success_url = reverse_lazy("app:media_list")
    login_url = "app:login"

    def get_queryset(self):
        # ユーザーが所有するファイルのみ削除可能
        return MediaFile.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
