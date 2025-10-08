import os
import time

from django.contrib.auth.models import AbstractUser
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils import timezone


class SafeMediaFileStorage(FileSystemStorage):
    """
    安全なメディアファイルストレージ
    """

    def get_available_name(self, name, max_length=None):
        """
        ファイル名を安全な形式に変換し、重複を避ける
        """
        # 絶対パスを相対パスに変換
        if os.path.isabs(name):
            name = os.path.basename(name)

        # ディレクトリとファイル名に分割
        dir_name = os.path.dirname(name)
        base_name = os.path.basename(name)
        safe_base_name = self._get_safe_filename(base_name)
        # ディレクトリが存在する場合は結合、そうでなければファイル名のみ
        safe_name = (
            os.path.join(dir_name, safe_base_name) if dir_name else safe_base_name
        )

        # 重複チェックのため元のget_available_nameメソッドを呼び出し
        return super().get_available_name(safe_name, max_length)

    def _get_safe_filename(self, filename):
        """
        ファイル名をタイムスタンプベースの安全な形式に変換
        """
        # ファイル拡張子を取得
        _, ext = os.path.splitext(filename)

        # タイムスタンプベースのファイル名を生成
        timestamp = int(time.time() * 1000)  # ミリ秒のタイムスタンプ

        # 安全なファイル名を生成
        safe_name = f"media_{timestamp}{ext}"

        return safe_name


class User(AbstractUser):
    """カスタムユーザーモデル"""

    email = models.EmailField(unique=True, verbose_name="メールアドレス")

    def __str__(self):
        return self.username


class Project(models.Model):
    """ユーザーごとのプロジェクト"""

    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="projects", verbose_name="オーナー"
    )
    name = models.CharField(max_length=100, verbose_name="プロジェクト名")
    description = models.TextField(blank=True, verbose_name="説明")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="作成日時")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")

    class Meta:
        verbose_name = "プロジェクト"
        verbose_name_plural = "プロジェクト"
        unique_together = ("owner", "name")
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


def media_upload_to(instance, filename):
    """ユーザー/プロジェクトのディレクトリへ保存するパスを返す"""
    user_part = f"user_{getattr(instance, 'user_id', None) or 'unknown'}"
    project_part = f"project_{getattr(instance, 'project_id', None) or 'unassigned'}"
    return os.path.join(user_part, project_part, filename)


class MediaFile(models.Model):
    """音声・動画ファイル用のモデル"""

    FILE_TYPE_CHOICES = [
        ("audio", "音声"),
        ("video", "動画"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="ユーザー")
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="media_files",
        verbose_name="プロジェクト",
        null=True,
        blank=True,
    )
    title = models.CharField(max_length=200, verbose_name="タイトル")
    description = models.TextField(blank=True, verbose_name="説明")
    file_type = models.CharField(
        max_length=10, choices=FILE_TYPE_CHOICES, verbose_name="ファイル種別"
    )
    file = models.FileField(
        upload_to=media_upload_to,
        storage=SafeMediaFileStorage(),
        verbose_name="ファイル",
    )
    file_size = models.PositiveIntegerField(verbose_name="ファイルサイズ（バイト）")
    duration = models.DurationField(null=True, blank=True, verbose_name="再生時間")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="作成日時")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")

    class Meta:
        verbose_name = "メディアファイル"
        verbose_name_plural = "メディアファイル"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.get_file_type_display()})"

    def get_file_size_mb(self):
        """ファイルサイズをMB単位で返す"""
        return round(self.file_size / (1024 * 1024), 2)

    def get_safe_filename(self):
        """安全なファイル名を取得"""
        if self.file:
            return os.path.basename(self.file.name)
        return ""

    def delete_physical_file(self):
        """
        メディアファイルの物理ファイルを削除
        """
        if self.file:
            try:
                file_path = self.file.path
                if os.path.exists(file_path):
                    os.remove(file_path)
                    print(f"メディアファイルを削除しました: {file_path}")

                    # ディレクトリが空になったら削除
                    file_dir = os.path.dirname(file_path)
                    if os.path.exists(file_dir) and not os.listdir(file_dir):
                        try:
                            os.rmdir(file_dir)
                            print(f"空のディレクトリを削除: {file_dir}")
                        except OSError:
                            pass  # ディレクトリが空でない場合は無視

            except (OSError, ValueError, AttributeError) as e:
                print(f"メディアファイル削除エラー: {e}")

    def delete(self, *args, **kwargs):
        """
        メディアファイルを完全に削除（ファイル、ディレクトリ、DB）
        物理ファイルの削除はpost_deleteシグナルで処理される
        """
        # データベースレコードを削除（シグナルで物理ファイルも削除される）
        super().delete(*args, **kwargs)


@receiver(post_delete, sender=MediaFile)
def delete_media_file(sender, instance, **kwargs):
    """
    メディアファイル削除時のシグナル
    物理ファイルとディレクトリを削除

    このシグナルはMediaFileモデルのレコードが削除された後に
    自動的に実行され、物理ファイルの削除を担当する。
    他の場所で手動でdelete_physical_file()を呼び出す必要はない。
    """
    # モデルのメソッドを再利用
    instance.delete_physical_file()
