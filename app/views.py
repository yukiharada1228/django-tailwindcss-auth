from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView as AuthLoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode
from django.views.generic import CreateView, TemplateView

from .forms import SignUpForm
from .models import User


class IndexView(LoginRequiredMixin, TemplateView):
    """ログイン必須のホームページ"""

    template_name = "index.html"
    login_url = "app:login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "title": "Django TailwindCSS",
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
