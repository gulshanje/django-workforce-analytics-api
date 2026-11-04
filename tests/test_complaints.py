import pytest
from rest_framework import status
from complaints.models import Complaint


@pytest.mark.django_db
class TestComplaintAPI:

    def test_create_complaint(self, authenticated_client):
        payload = {
            "employee_id": 1,
            "title": "Printer broken",
            "description": "The printer on floor 3 is not working",
        }
        response = authenticated_client.post("/api/complaints/", payload)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["title"] == "Printer broken"
        # Priority should be auto-predicted
        assert response.data["priority"] in ["low", "medium", "high"]

    def test_search_complaints_by_keyword(self, authenticated_client):
        Complaint.objects.create(
            employee_id=1, title="Network issue", description="VPN disconnects"
        )
        Complaint.objects.create(
            employee_id=2, title="Coffee machine", description="Out of beans"
        )

        response = authenticated_client.get("/api/complaints/?keyword=network")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["title"] == "Network issue"

    def test_update_status(self, authenticated_client):
        complaint = Complaint.objects.create(
            employee_id=1, title="Test", description="Test", status="open"
        )
        response = authenticated_client.patch(
            f"/api/complaints/{complaint.id}/update_status/",
            {"status": "closed"},
        )
        assert response.status_code == status.HTTP_200_OK
        complaint.refresh_from_db()
        assert complaint.status == "closed"

    def test_update_status_invalid_fails(self, authenticated_client):
        complaint = Complaint.objects.create(
            employee_id=1, title="Test", description="Test"
        )
        response = authenticated_client.patch(
            f"/api/complaints/{complaint.id}/update_status/",
            {"status": "invalid_status"},
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST