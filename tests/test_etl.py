import pytest
from datetime import timedelta
from django.utils import timezone
from django.core.management import call_command

from attendance.models import Attendance
from complaints.models import Complaint
from etl.models import ETLRunLog, FactAttendance, FactComplaint


@pytest.mark.django_db
class TestETLPipeline:

    def test_etl_loads_completed_attendance(self):
        now = timezone.now()
        Attendance.objects.create(
            employee_id=1,
            check_in=now - timedelta(hours=8),
            check_out=now - timedelta(hours=1),
        )
        call_command("run_etl")

        assert FactAttendance.objects.count() == 1
        fact = FactAttendance.objects.first()
        assert fact.employee_id == 1
        assert fact.duration_hours == 7.0
        assert ETLRunLog.objects.filter(status="success").exists()

    def test_etl_ignores_open_attendance(self):
        Attendance.objects.create(
            employee_id=1, check_in=timezone.now(), check_out=None
        )
        call_command("run_etl")
        assert FactAttendance.objects.count() == 0

    def test_etl_loads_complaints(self):
        Complaint.objects.create(
            employee_id=1, title="Test", description="Test", priority="high"
        )
        call_command("run_etl")
        assert FactComplaint.objects.count() == 1
        assert FactComplaint.objects.first().priority == "high"

    def test_etl_is_idempotent(self):
        now = timezone.now()
        Attendance.objects.create(
            employee_id=1,
            check_in=now - timedelta(hours=8),
            check_out=now - timedelta(hours=1),
        )
        call_command("run_etl")
        call_command("run_etl")
        assert FactAttendance.objects.count() == 1

    def test_etl_logs_failure(self, monkeypatch):
        def boom(*args, **kwargs):
            raise RuntimeError("simulated failure")

        monkeypatch.setattr(
            "etl.management.commands.run_etl.FactAttendance.objects.update_or_create",
            boom,
        )
        Attendance.objects.create(
            employee_id=1,
            check_in=timezone.now() - timedelta(hours=2),
            check_out=timezone.now() - timedelta(hours=1),
        )
        with pytest.raises(RuntimeError):
            call_command("run_etl")
        run = ETLRunLog.objects.first()
        assert run.status == "failed"
        assert "simulated failure" in run.error_message