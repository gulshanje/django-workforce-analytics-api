import pytest
from rest_framework import status
from attendance.models import Attendance


@pytest.mark.django_db
class TestAttendanceAPI:

    def test_check_in_requires_auth(self, api_client):
        response = api_client.post("/api/attendance/check_in/", {"employee_id": 1})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_check_in_creates_record(self, authenticated_client):
        response = authenticated_client.post(
            "/api/attendance/check_in/", {"employee_id": 1}
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert Attendance.objects.filter(employee_id=1, check_out__isnull=True).exists()

    def test_check_out_closes_open_record(self, authenticated_client):
        # First check in
        authenticated_client.post("/api/attendance/check_in/", {"employee_id": 1})

        # Then check out
        response = authenticated_client.post(
            "/api/attendance/check_out/", {"employee_id": 1}
        )
        assert response.status_code == status.HTTP_200_OK
        record = Attendance.objects.get(employee_id=1)
        assert record.check_out is not None

    def test_check_out_without_check_in_fails(self, authenticated_client):
        response = authenticated_client.post(
            "/api/attendance/check_out/", {"employee_id": 99}
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST