from django.contrib import admin
from .models import Attendance


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("employee_id", "check_in", "check_out")
    list_filter = ("check_in",)
    search_fields = ("employee_id",)
