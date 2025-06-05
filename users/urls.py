from django.urls import path
from .views import (
    RegisterView, LoginView, UserProfileView, UserListView,
    TechnicianAssignedIssuesView, UserCreatedIssuesView,
    IssueCommentListCreateView, IssueFeedbackView, IssueListCreateView,
    CreateUserView, ChangeUserRoleView, DeleteUserView,
    logout_view, ChangePasswordView,  # ✅ Buraya ekledik
)

from users.views_admin import (
    TechnicianPerformanceExcelView,
    IssueReportExcelView,
    IssueReportPDFView,
    TechnicianPerformanceView,
    IssueStatisticsView,
)

from users.views import (
    AdminUserListView,
    IssueAttachmentUploadView,
    IssueAttachmentListView,
    IssueDetailView,
    TwitterRedirectDirectView,
    TwitterRedirectView,
    TechnicianAssignedIssuesView,
    TechnicianListView,
)

urlpatterns = [
    # ✅ Kimlik Doğrulama & Kullanıcı Yönetimi
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),  # ✅ EKLENDİ
    path("me/", UserProfileView.as_view(), name="user-profile"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),  # ✅ EKLENDİ
    path("", UserListView.as_view(), name="user-list"),
    path("create/", CreateUserView.as_view(), name="create-user"),
    path("change-role/", ChangeUserRoleView.as_view(), name="change-user-role"),
    path("delete/<int:pk>/", DeleteUserView.as_view(), name="delete-user"),
    path("list/", UserListView.as_view(), name="user-list"),

    # ✅ Arıza API'leri
    path("issues/", IssueListCreateView.as_view(), name="issue-list-create"),
    path("issues/assigned/", TechnicianAssignedIssuesView.as_view(), name="assigned-issues"),
    path("issues/my/", UserCreatedIssuesView.as_view(), name="my-issues"),
    path("issues/<int:pk>/comments/", IssueCommentListCreateView.as_view(), name="issue-comments"),
    path("issues/<int:pk>/feedback/", IssueFeedbackView.as_view(), name="issue-feedback"),

    # ✅ Arıza Fotoğraf Yükleme & Listeleme
    path("issues/<int:pk>/upload/", IssueAttachmentUploadView.as_view(), name="upload-attachment"),
    path("issues/<int:pk>/attachments/", IssueAttachmentListView.as_view(), name="list-attachments"),

    # ✅ Admin Yetkilendirme
    path("admin/users/", AdminUserListView.as_view(), name="admin-user-list"),
    path("admin/create-user/", CreateUserView.as_view(), name="create-user"),
    path("admin/change-role/", ChangeUserRoleView.as_view(), name="change-user-role"),

    # ✅ Teknisyen & Arıza İstatistikleri
    path("admin/technician-stats/", TechnicianPerformanceView.as_view(), name="technician-stats"),
    path("admin/issue-stats/", IssueStatisticsView.as_view(), name="issue-stats"),

    # ✅ Excel & PDF Raporları
    path("admin/reports/technician-excel/", TechnicianPerformanceExcelView.as_view(), name="technician-excel"),
    path("admin/reports/issues-excel/", IssueReportExcelView.as_view(), name="issues-excel"),
    path("admin/reports/issues-pdf/", IssueReportPDFView.as_view(), name="issues-pdf"),

    path("api/issues/<int:pk>/", IssueDetailView.as_view(), name="issue-detail"),

    path("api/custom-twitter-login/", TwitterRedirectDirectView.as_view(), name="custom-twitter-login"),
    path("api/custom-twitter-login/", TwitterRedirectView.as_view(), name="custom-twitter-login"),

    path("technician/issues/", TechnicianAssignedIssuesView.as_view(), name="technician-issues"),
    path('assigned-issues/', TechnicianAssignedIssuesView.as_view(), name='technician-assigned-issues'),

    path('technicians/', TechnicianListView.as_view(), name='technician-list'),
]
