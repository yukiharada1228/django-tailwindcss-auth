from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """カスタムユーザーモデル"""

    email = models.EmailField(unique=True, verbose_name="メールアドレス")

    def __str__(self):
        return self.username
