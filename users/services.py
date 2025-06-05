from django.db.models import Avg, Count, F
from .models import Issue, CustomUser


def get_best_technician_for_category(category):
    """Aynı kategorideki arızaları en hızlı çözen teknisyeni bul"""
    technicians = CustomUser.objects.filter(role="technician")

    # Teknisyenlerin çözüm sürelerini hesapla
    tech_performance = (
        Issue.objects.filter(category=category, status="resolved", assigned_to__in=technicians)
        .values("assigned_to")
        .annotate(avg_resolution_time=Avg(F("resolved_at") - F("created_at")))
        .order_by("avg_resolution_time")
    )

    if tech_performance.exists():
        best_tech_id = tech_performance.first()["assigned_to"]
        return CustomUser.objects.get(id=best_tech_id)

    # Eğer veri yoksa en az aktif arızası olanı seç
    return technicians.annotate(issue_count=Count("assigned_issues")).order_by("issue_count").first()
