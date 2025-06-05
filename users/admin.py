from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Issue, IssueAttachment  # Yeni modelleri ekledik

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ("email", "is_staff", "is_superuser")
    search_fields = ("email",)
    ordering = ("email",)  # username yerine email kullanılıyor

    # Kullanıcı adı alanını kaldırıp, e-posta ile giriş yapılmasını sağlıyoruz.
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_superuser")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "is_staff", "is_superuser"),
        }),
    )

# 🔹 Arıza Modeli Admin Panel Kaydı
@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "priority", "created_at", "assigned_to")
    search_fields = ("title", "description")
    list_filter = ("status", "priority", "created_at")
    ordering = ("-created_at",)

# 🔹 Arıza Görselleri Admin Panel Kaydı
@admin.register(IssueAttachment)
class IssueAttachmentAdmin(admin.ModelAdmin):
    list_display = ("issue", "image")
