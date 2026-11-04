from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from attendance.models import Attendance
from complaints.models import Complaint
from etl.models import ETLRunLog, FactAttendance, FactComplaint


class Command(BaseCommand):
    help = "Run the attendance and complaint ETL pipeline"

    def handle(self, *args, **options):
        run = ETLRunLog.objects.create(pipeline_name="attendance_complaints")
        try:
            # Use the last successful run as the watermark for incremental extraction
            last_run = (
                ETLRunLog.objects.filter(
                    pipeline_name="attendance_complaints", status="success"
                )
                .exclude(pk=run.pk)
                .order_by("-finished_at")
                .first()
            )
            since = last_run.finished_at if last_run else timezone.now() - timedelta(days=30)

            extracted = 0
            loaded = 0

            # ---- Attendance ----
            att_qs = Attendance.objects.filter(
                check_out__isnull=False, check_out__gte=since
            )
            for rec in att_qs.iterator():
                extracted += 1
                duration = (rec.check_out - rec.check_in).total_seconds() / 3600.0
                FactAttendance.objects.update_or_create(
                    source_attendance_id=rec.id,
                    defaults={
                        "employee_id": rec.employee_id,
                        "date": rec.check_in.date(),
                        "check_in": rec.check_in,
                        "check_out": rec.check_out,
                        "duration_hours": round(duration, 2),
                    },
                )
                loaded += 1

            # ---- Complaints ----
            cmp_qs = Complaint.objects.filter(updated_at__gte=since)
            for rec in cmp_qs.iterator():
                extracted += 1
                FactComplaint.objects.update_or_create(
                    source_complaint_id=rec.id,
                    defaults={
                        "employee_id": rec.employee_id,
                        "title": rec.title,
                        "status": rec.status,
                        "priority": rec.priority or "unknown",
                        "created_at": rec.created_at,
                    },
                )
                loaded += 1

            run.rows_extracted = extracted
            run.rows_loaded = loaded
            run.status = "success"
            run.finished_at = timezone.now()
            run.save()
            self.stdout.write(
                self.style.SUCCESS(
                    f"ETL complete: extracted={extracted}, loaded={loaded}"
                )
            )
        except Exception as exc:
            run.status = "failed"
            run.error_message = str(exc)
            run.finished_at = timezone.now()
            run.save()
            self.stderr.write(self.style.ERROR(f"ETL failed: {exc}"))
            raise