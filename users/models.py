from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, AbstractUser, Group, \
    Permission
from django.db import models
from django.utils.timezone import now
from django.db.models import Count



class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Yeni bir kullanıcı oluşturur"""
        if not email:
            raise ValueError("Email adresi gereklidir.")
        email = self.normalize_email(email)
        extra_fields.setdefault("role", "user")  # Varsayılan rol kullanıcı olsun
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Yeni bir süper kullanıcı oluşturur"""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", "admin")  # Süper kullanıcı admin olur
        return self.create_user(email, password, **extra_fields)


from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models

# 🔹 Kullanıcı Modeli
class CustomUser(AbstractBaseUser, PermissionsMixin):
    class RoleChoices(models.TextChoices):
        ADMIN = "admin", "Admin"
        TECHNICIAN = "technician", "Teknisyen"
        USER = "user", "Kullanıcı"

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    #role alanını veritabanında saklar
    role = models.CharField(
        max_length=20,
        choices=RoleChoices.choices,
        default=RoleChoices.USER,
    )

    assigned_area = models.CharField(max_length=255, blank=True, null=True)

    # 📌 Çakışmayı önlemek için related_name ekledik
    groups = models.ManyToManyField(Group, related_name="customuser_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="customuser_permissions", blank=True)

    objects = BaseUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email} - {self.get_role_display()}"  # ✅ `get_role_display()` ile okunabilir hale getir



# 🔹 Arıza Modeli (Issue)
class Issue(models.Model):
    STATUS_CHOICES = [
        ("pending", "Beklemede"),
        ("in_progress", "İnceleniyor"),
        ("resolved", "Çözüldü"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="issues")
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name="assigned_issues")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    priority = models.CharField(max_length=10, default="medium")
    category = models.CharField(max_length=50, default="Diğer")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # ✅ Yeni Alan: Çözüm Süresi (Arızanın çözüldüğü tarih ve saat)
    resolved_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        """Otomatik teknisyen atama ve durum güncelleme sistemi"""
        if not self.assigned_to and self.category:
            available_technicians = CustomUser.objects.filter(role="technician").annotate(
                issue_count=Count("assigned_issues")
            ).order_by("issue_count")  # En az iş yükü olan teknisyeni seç

            if available_technicians.exists():
                self.assigned_to = available_technicians.first()

        # Eğer arıza "Çözüldü" durumuna geçtiyse, çözüldüğü zaman kaydedilsin
        if self.status == "resolved" and not self.resolved_at:
            self.resolved_at = now()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.status}"


# 🔹 Arıza Yorumları Modeli (IssueComment)
class IssueComment(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Yorum: {self.user.email} - {self.issue.title}"


# 🔹 Arıza İçin Fotoğraf Modeli (IssueAttachment)
class IssueAttachment(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name="attachments")
    image = models.ImageField(upload_to="issue_images/")

    def __str__(self):
        return f"Eklenen Görsel - {self.issue.title}"