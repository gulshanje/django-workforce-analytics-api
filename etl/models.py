from django.db import models


class ETLRunLog(models.Model):
    pipeline_name = models.CharField(max_length=100)
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, default="running")
    rows_extracted = models.IntegerField(default=0)
    rows_loaded = models.IntegerField(default=0)
    error_message = models.TextField(blank=True)

    class Meta:
        ordering = ["-started_at"]

    def __str__(self):
        return f"{self.pipeline_name} @ {self.started_at} [{self.status}]"


class FactAttendance(models.Model):
    """Warehouse table: one row per completed attendance record."""
    employee_id = models.IntegerField()
    date = models.DateField()
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    duration_hours = models.FloatField()
    source_attendance_id = models.IntegerField(unique=True)
    loaded_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=["employee_id", "date"])]


class FactComplaint(models.Model):
    """Warehouse table: complaints enriched with predicted priority."""
    source_complaint_id = models.IntegerField(unique=True)
    employee_id = models.IntegerField()
    title = models.CharField(max_length=200)
    status = models.CharField(max_length=20)
    priority = models.CharField(max_length=10)
    created_at = models.DateTimeField()
    loaded_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=["priority", "status"])]