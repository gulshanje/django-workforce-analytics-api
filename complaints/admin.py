from django.contrib import admin
from .models import Complaint


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ("title", "employee_id", "status", "priority", "created_at")
    list_filter = ("status", "priority", "created_at")
    search_fields = ("title", "description", "employee_id")
