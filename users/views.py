import logging
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from django.db.models import Count
from django.contrib.auth import authenticate, login, logout
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import viewsets
from rest_framework import generics, permissions
from users.models import Issue
from users.serializers import IssueSerializer
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics
from users.models import CustomUser
from users.serializers import UserSerializer

from users.models import CustomUser, Issue, IssueAttachment, IssueComment
from users.serializers import (
    IssueSerializer, RegisterSerializer, LoginSerializer, UserSerializer,
    IssueCommentSerializer, AdminCreateUserSerializer, UserRoleUpdateSerializer,
    IssueAttachmentSerializer
)
from users.ml_model import predict_category, analyze_sentiment, assign_technician

logging.basicConfig(level=logging.INFO)

# ✅ Oturum Yönetimi
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_view(request):
    logout(request)
    return Response({"message": "Çıkış yapıldı"}, status=status.HTTP_200_OK)

from django.contrib.auth import login, authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.serializers import UserSerializer
from users.models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    }

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)

            # JWT token üret
            tokens = get_tokens_for_user(user)

            # Kullanıcı bilgilerini al
            serializer = UserSerializer(user)
            user_data = serializer.data

            # token'ları yanıt içine ekle
            refresh = RefreshToken.for_user(user)
            user_data["access"] = tokens["access"]
            user_data["refresh"] = tokens["refresh"]

            print("✅ Backend Giriş Yanıtı:", user_data)

            return Response(user_data, status=200)
        else:
            return Response({"error": "Geçersiz e-posta veya şifre."}, status=401)


class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.is_authenticated:
            return Response({"error": "Giriş yapılmamış"}, status=401)

        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        if not user.check_password(old_password):
            return Response({"error": "Eski şifre yanlış."}, status=400)

        if not new_password or len(new_password) < 6:
            return Response({"error": "Yeni şifre en az 6 karakter olmalı."}, status=400)

        user.set_password(new_password)
        user.save()
        return Response({"message": "Şifre başarıyla güncellendi."}, status=200)

# ✅ Kullanıcı Yönetimi
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

class CreateUserView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = AdminCreateUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Kullanıcı başarıyla oluşturuldu."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChangeUserRoleView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        user_id = request.data.get("user_id")
        new_role = request.data.get("role")

        if new_role not in ["admin", "technician", "user"]:
            return Response({"error": "Geçersiz rol."}, status=400)

        try:
            user = CustomUser.objects.get(id=user_id)
            user.role = new_role
            user.is_staff = new_role in ["admin", "technician"]
            user.is_superuser = new_role == "admin"
            user.save()
            return Response({"message": f"{user.email} kullanıcısının rolü {new_role} olarak güncellendi."})
        except CustomUser.DoesNotExist:
            return Response({"error": "Kullanıcı bulunamadı."}, status=404)

class DeleteUserView(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, pk):
        try:
            user = CustomUser.objects.get(pk=pk)
            if user == request.user:
                return Response({"error": "Admin kendi hesabını silemez."}, status=400)
            user.delete()
            return Response({"message": "Kullanıcı başarıyla silindi."}, status=200)
        except CustomUser.DoesNotExist:
            return Response({"error": "Kullanıcı bulunamadı."}, status=404)

# ✅ Arıza API'leri
class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class IssueListCreateView(generics.ListCreateAPIView):
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Issue.objects.all()
        elif user.role == 'technician':
            return Issue.objects.filter(assigned_to=user)
        else:
            return Issue.objects.filter(created_by=user)
        print("🔐 Giriş yapan kullanıcı:", self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class IssueDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        issue = self.get_object()
        if request.user != issue.created_by and request.user.role not in ["admin", "technician"]:
            return Response({"error": "Bu işlemi gerçekleştirme yetkiniz yok."}, status=403)
        return super().update(request, *args, **kwargs)


class TechnicianAssignedIssuesView(generics.ListAPIView):
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Issue.objects.filter(assigned_to=self.request.user)

class UserCreatedIssuesView(generics.ListAPIView):
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Issue.objects.filter(created_by=self.request.user)

class IssueCommentListCreateView(generics.ListCreateAPIView):
    serializer_class = IssueCommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        issue_id = self.kwargs["pk"]
        return IssueComment.objects.filter(issue_id=issue_id)

    def perform_create(self, serializer):
        issue = Issue.objects.get(pk=self.kwargs["pk"])
        serializer.save(issue=issue, user=self.request.user)

class IssueFeedbackView(generics.UpdateAPIView):
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Issue.objects.filter(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(created_by=self.request.user)

class IssueAttachmentUploadView(generics.CreateAPIView):
    queryset = IssueAttachment.objects.all()
    serializer_class = IssueAttachmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        issue_id = self.kwargs["pk"]
        try:
            issue = Issue.objects.get(id=issue_id)
            if self.request.user != issue.created_by and self.request.user != issue.assigned_to:
                raise PermissionError("Bu arızaya fotoğraf ekleme yetkiniz yok.")
            serializer.save(issue=issue)
        except Issue.DoesNotExist:
            raise ValidationError({"error": "Arıza bulunamadı."})


class IssueAttachmentListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            issue = Issue.objects.get(pk=pk)
            if request.user != issue.created_by and request.user != issue.assigned_to:
                return Response({"error": "Yetkisiz işlem"}, status=status.HTTP_403_FORBIDDEN)
            attachments = IssueAttachment.objects.filter(issue=issue)
            serializer = IssueAttachmentSerializer(attachments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Issue.DoesNotExist:
            return Response({"error": "Arıza bulunamadı"}, status=status.HTTP_404_NOT_FOUND)

class AdminUserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


from rest_framework.views import APIView
from django.shortcuts import redirect
from django.conf import settings

from rest_framework.permissions import AllowAny

class GoogleRedirectDirectView(APIView):
    permission_classes = [AllowAny]  # ✅ Giriş yapmadan erişilsin

    def get(self, request):
        redirect_url = (
            "https://accounts.google.com/o/oauth2/v2/auth"
            f"?client_id={settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY}"
            f"&redirect_uri=http://127.0.0.1:8000/accounts/google/login/callback/"
            "&response_type=code"
            "&scope=openid%20email%20profile"
        )
        return redirect(redirect_url)


class TechnicianListView(generics.ListAPIView):
    queryset = CustomUser.objects.filter(role="technician")
    serializer_class = UserSerializer

# views.py
class TwitterRedirectView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        redirect_url = (
            "https://twitter.com/i/oauth2/authorize"
            f"?response_type=code"
            f"&client_id={settings.SOCIAL_AUTH_TWITTER_KEY}"
            f"&redirect_uri=http://127.0.0.1:8000/accounts/twitter/login/callback/"
            f"&scope=tweet.read%20users.read"
            f"&state=randomstate"
            f"&code_challenge=challenge"
            f"&code_challenge_method=plain"
        )
        return redirect(redirect_url)

class TwitterRedirectDirectView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        redirect_url = (
            "https://twitter.com/i/oauth2/authorize"
            f"?client_id={settings.SOCIAL_AUTH_TWITTER_KEY}"
            f"&redirect_uri=http://127.0.0.1:8000/accounts/twitter/login/callback/"
            "&response_type=code"
            "&scope=tweet.read%20users.read%20offline.access"
        )
        return redirect(redirect_url)



# JWT View artık kullanılmıyor – pasifleştirildi
# class CustomTokenObtainPairView(TokenObtainPairView):
#     def post(self, request, *args, **kwargs):
#         response = super().post(request, *args, **kwargs)
#         user = CustomUser.objects.get(email=request.data.get("email"))
#         if response.status_code == 200:
#             response.data["role"] = user.role
#         return response