from django.contrib import admin
from .models import ETLRunLog, FactAttendance, FactComplaint


@admin.register(ETLRunLog)
class ETLRunLogAdmin(admin.ModelAdmin):
    list_display = (
        "pipeline_name",
        "status",
        "started_at",
        "finished_at",
        "rows_extracted",
        "rows_loaded",
    )
    list_filter = ("status", "pipeline_name")
    search_fields = ("pipeline_name", "error_message")
    readonly_fields = ("started_at", "finished_at")


@admin.register(FactAttendance)
class FactAttendanceAdmin(admin.ModelAdmin):
    list_display = (
        "employee_id",
        "date",
        "check_in",
        "check_out",
        "duration_hours",
        "source_attendance_id",
    )
    list_filter = ("date",)
    search_fields = ("employee_id", "source_attendance_id")
    readonly_fields = ("loaded_at",)


@admin.register(FactComplaint)
class FactComplaintAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "employee_id",
        "status",
        "priority",
        "created_at",
        "source_complaint_id",
    )
    list_filter = ("status", "priority", "created_at")
    search_fields = ("title", "employee_id", "source_complaint_id")
    readonly_fields = ("loaded_at",)
