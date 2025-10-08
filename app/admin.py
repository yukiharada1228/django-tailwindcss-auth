from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import Project, User

# 管理画面のタイトル設定
admin.site.site_header = "Django TailwindCSS Multimedia Auth 管理画面"
admin.site.site_title = "管理画面"
admin.site.index_title = "サイト管理"


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """カスタムユーザー管理"""

    # リスト表示のフィールド
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
        "date_joined",
    )
    list_filter = ("is_staff", "is_superuser", "is_active", "date_joined")
    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("-date_joined",)

    # 詳細表示のフィールド
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    # 追加・編集時のフィールド
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "password1", "password2"),
            },
        ),
    )

    # 読み取り専用フィールド
    readonly_fields = ("date_joined", "last_login")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "created_at", "updated_at")
    list_filter = ("owner", "created_at")
    search_fields = ("name", "description", "owner__username", "owner__email")
