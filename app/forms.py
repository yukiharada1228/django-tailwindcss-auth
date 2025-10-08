from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .models import MediaFile
from .urls import ACCOUNTS_PREFIX

User = get_user_model()


class SignUpForm(UserCreationForm):
    """サインアップフォーム"""

    email = forms.EmailField(
        label="メールアドレス",
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": "w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",
                "placeholder": "メールアドレスを入力",
            }
        ),
    )
    username = forms.CharField(
        label="ユーザー名",
        widget=forms.TextInput(
            attrs={
                "class": "w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",
                "placeholder": "ユーザー名を入力",
            }
        ),
    )
    password1 = forms.CharField(
        label="パスワード",
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",
                "placeholder": "パスワードを入力",
            }
        ),
    )
    password2 = forms.CharField(
        label="パスワード（確認）",
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",
                "placeholder": "パスワードを再入力",
            }
        ),
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("このメールアドレスは既に登録されています。")
        return email

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("このユーザー名は既に使用されています。")
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.is_active = False  # アクティベーションが必要
        if commit:
            user.save()
            self._send_activation_email(user)
        return user

    def _send_activation_email(self, user):
        subject = "[Django TailwindCSS Multimedia Auth] 仮登録完了のお知らせ"
        message_template = """
Django TailwindCSS Multimedia Auth にご登録いただきありがとうございます。
以下のURLをクリックして、本登録を完了してください。

"""
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        activate_url = settings.FRONTEND_URL + f"/{ACCOUNTS_PREFIX}activate/{uid}/{token}/"
        message = message_template + activate_url
        user.email_user(subject, message)


class MediaFileUploadForm(forms.ModelForm):
    """メディアファイルアップロードフォーム"""

    class Meta:
        model = MediaFile
        fields = ["title", "description", "file_type", "file"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",
                    "placeholder": "ファイルのタイトルを入力",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",
                    "rows": 3,
                    "placeholder": "ファイルの説明を入力（任意）",
                }
            ),
            "file_type": forms.Select(
                attrs={
                    "class": "w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                }
            ),
            "file": forms.FileInput(
                attrs={
                    "class": "w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",
                    "accept": "audio/*,video/*",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].label = "タイトル"
        self.fields["description"].label = "説明"
        self.fields["file_type"].label = "ファイル種別"
        self.fields["file"].label = "ファイル"

    def clean_file(self):
        file = self.cleaned_data.get("file")
        if file:
            # ファイルサイズ制限（100MB）
            max_size = 100 * 1024 * 1024  # 100MB
            if file.size > max_size:
                raise forms.ValidationError(
                    "ファイルサイズが大きすぎます。100MB以下のファイルを選択してください。"
                )

            # ファイル形式の検証
            file_type = self.cleaned_data.get("file_type")
            if file_type == "audio":
                if not file.content_type.startswith("audio/"):
                    raise forms.ValidationError("音声ファイルを選択してください。")
            elif file_type == "video":
                if not file.content_type.startswith("video/"):
                    raise forms.ValidationError("動画ファイルを選択してください。")

        return file


class MediaFileRenameForm(forms.ModelForm):
    """メディアファイル名変更フォーム"""

    class Meta:
        model = MediaFile
        fields = ["title"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",
                    "placeholder": "新しいファイル名を入力",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].label = "ファイル名"
