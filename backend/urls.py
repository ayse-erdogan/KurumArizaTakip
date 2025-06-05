from django.contrib import admin
from users.views import TwitterRedirectDirectView
from django.urls import path, include
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.twitter.views import TwitterOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static
from users.views import IssueListCreateView, IssueDetailView, LoginView, logout_view, UserDetailView
from users.views import GoogleRedirectDirectView
from rest_framework_simplejwt.views import TokenRefreshView

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client


class TwitterLogin(SocialLoginView):
    adapter_class = TwitterOAuth2Adapter
    client_class = OAuth2Client


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    # Kullanıcı uygulamanın kendi url'leri (giriş/kayıt/logout)
    path('api/auth/login/', LoginView.as_view(), name='login'),
    path('api/auth/logout/', logout_view, name='logout'),
    path('api/auth/user/', UserDetailView.as_view(), name='user-detail'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Diğer User endpointleri
    path('api/users/', include('users.urls')),

    # JWT (opsiyonel, eğer kullanmayacaksan kaldır)
    path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Sosyal girişler (Google, Twitter gibi)
    path('api/auth/social/google/', GoogleLogin.as_view(), name='google_login'),
    path('api/auth/social/twitter/', TwitterLogin.as_view(), name='twitter_login'),

    # Issue endpointleri
    path("api/issues/", IssueListCreateView.as_view(), name="issue-list"),
    path("api/issues/<int:pk>/", IssueDetailView.as_view(), name="issue-detail"),

    path("api/custom-google-login/", GoogleRedirectDirectView.as_view(), name="custom-google-login"),
    path("api/custom-twitter-login/", TwitterRedirectDirectView.as_view(), name="custom-twitter-login")



]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
