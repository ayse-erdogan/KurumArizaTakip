from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.db.models import Count, Avg, ExpressionWrapper, F, DurationField
from users.models import CustomUser, Issue,IssueAttachment
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from users.serializers import IssueAttachmentSerializer
from django.db.models import DurationField
import pandas as pd
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from reportlab.pdfgen import canvas
from users.models import Issue, CustomUser
from datetime import datetime



# ✅ Teknisyen Performans Analizi API'si
class TechnicianPerformanceView(APIView):
    permission_classes = [IsAuthenticated]  # Sadece admin erişebilir

    def get(self, request):
        technicians = CustomUser.objects.filter(role="technician").annotate(
            total_issues=Count("assigned_issues"),
            avg_resolution_time=Avg(
                ExpressionWrapper(
                    F("assigned_issues__resolved_at") - F("assigned_issues__created_at"),
                    output_field=DurationField(),
                )
            )
        )

        data = [
            {
                "id": tech.id,
                "name": tech.name,
                "email": tech.email,
                "total_issues": tech.total_issues,
                "avg_resolution_time": tech.avg_resolution_time.total_seconds() if tech.avg_resolution_time else "No Resolved Issues"
            }
            for tech in technicians
        ]
        return Response(data)

# ✅ Genel Arıza İstatistikleri API'si
class IssueStatisticsView(APIView):
    permission_classes = [IsAdminUser]  # Sadece admin erişebilir

    def get(self, request):
        total_issues = Issue.objects.count()
        open_issues = Issue.objects.filter(status="pending").count()
        closed_issues = Issue.objects.filter(status="resolved").count()
        most_common_category = Issue.objects.values("category").annotate(count=Count("category")).order_by("-count").first()

        data = {
            "total_issues": total_issues,
            "open_issues": open_issues,
            "closed_issues": closed_issues,
            "most_common_category": most_common_category["category"] if most_common_category else "N/A"
        }
        return Response(data)



class IssueAttachmentUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, pk):
        """Arızaya fotoğraf ekler"""
        try:
            issue = Issue.objects.get(pk=pk)

            # Kullanıcı arızanın sahibi mi veya atanmış teknisyen mi kontrol et
            if request.user != issue.created_by and request.user != issue.assigned_to:
                return Response({"error": "Yetkisiz işlem"}, status=status.HTTP_403_FORBIDDEN)

            file_serializer = IssueAttachmentSerializer(data=request.data)
            if file_serializer.is_valid():
                file_serializer.save(issue=issue)
                return Response(file_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Issue.DoesNotExist:
            return Response({"error": "Arıza bulunamadı"}, status=status.HTTP_404_NOT_FOUND)


class IssueAttachmentListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        """Belirtilen arızaya ait fotoğrafları getirir"""
        try:
            issue = Issue.objects.get(pk=pk)

            # Kullanıcı yetkili mi kontrol et
            if request.user != issue.created_by and request.user != issue.assigned_to:
                return Response({"error": "Yetkisiz işlem"}, status=status.HTTP_403_FORBIDDEN)

            attachments = IssueAttachment.objects.filter(issue=issue)
            serializer = IssueAttachmentSerializer(attachments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Issue.DoesNotExist:
            return Response({"error": "Arıza bulunamadı"}, status=status.HTTP_404_NOT_FOUND)




class TechnicianPerformanceExcelView(APIView):
    permission_classes = [IsAdminUser]  # Sadece admin erişebilir

    def get(self, request):
        """Teknisyen performanslarını Excel formatında indirir"""
        technicians = CustomUser.objects.filter(role="technician").values(
            "name", "email"
        ).annotate(total_issues=Count("assigned_issues"))

        df = pd.DataFrame(list(technicians))
        df.columns = ["Ad", "E-posta", "Çözülen Arıza Sayısı"]

        response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response["Content-Disposition"] = 'attachment; filename="teknisyen_performans.xlsx"'
        df.to_excel(response, index=False, engine="openpyxl")
        return response


class IssueReportExcelView(APIView):
    permission_classes = [IsAuthenticated]  # Sadece admin erişebilir

    def get(self, request):
        """Belirtilen tarih aralığındaki arıza kayıtlarını Excel formatında indirir"""
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")

        issues = Issue.objects.all()
        if start_date and end_date:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
            issues = issues.filter(created_at__range=[start_date, end_date])

        data = [
            {
                "Başlık": issue.title,
                "Açıklama": issue.description,
                "Durum": issue.get_status_display(),
                "Öncelik": issue.priority,
                "Kategori": issue.category,
                "Oluşturma Tarihi": issue.created_at.strftime("%Y-%m-%d"),
                "Atanan Teknisyen": issue.assigned_to.name if issue.assigned_to else "Atanmadı",
            }
            for issue in issues
        ]

        df = pd.DataFrame(data)
        response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response["Content-Disposition"] = 'attachment; filename="ariza_raporu.xlsx"'
        df.to_excel(response, index=False, engine="openpyxl")
        return response


class IssueReportPDFView(APIView):
    permission_classes = [IsAuthenticated]  # Sadece admin erişebilir

    def get(self, request):
        """Arıza kayıtlarını PDF formatında indirir"""
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="ariza_raporu.pdf"'

        p = canvas.Canvas(response)
        p.setFont("Helvetica", 12)
        p.drawString(100, 800, "Arıza Raporu")

        issues = Issue.objects.all()
        y_position = 780

        for issue in issues:
            p.drawString(100, y_position, f"{issue.title} - {issue.get_status_display()} ({issue.created_at.strftime('%Y-%m-%d')})")
            y_position -= 20
            if y_position < 100:
                p.showPage()
                y_position = 800

        p.save()
        return response
