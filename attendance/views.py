from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from .models import Attendance
from .serializers import AttendanceSerializer

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all().order_by("-check_in")
    serializer_class = AttendanceSerializer

    @action(detail=False, methods=["post"])
    def check_in(self, request):
        employee_id = request.data.get("employee_id")
        if not employee_id:
            return Response({"error": "employee_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        record = Attendance.objects.create(
            employee_id=employee_id,
            check_in=timezone.now(),
        )
        return Response(AttendanceSerializer(record).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["post"])
    def check_out(self, request):
        employee_id = request.data.get("employee_id")
        record = Attendance.objects.filter(
            employee_id=employee_id, check_out__isnull=True
        ).order_by("-check_in").first()
        if not record:
            return Response({"error": "No open check-in found"}, status=status.HTTP_400_BAD_REQUEST)
        record.check_out = timezone.now()
        record.save()
        return Response(AttendanceSerializer(record).data)