import pytest
from rest_framework import status


@pytest.mark.django_db
class TestPredictorAPI:

    def test_predict_requires_auth(self, api_client):
        response = api_client.post(
            "/api/predict/priority/", {"text": "Server down"}
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_predict_returns_priority(self, authenticated_client):
        response = authenticated_client.post(
            "/api/predict/priority/",
            {"text": "Production server is down and customers cannot log in"},
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data["priority"] in ["low", "medium", "high"]

    def test_predict_empty_text_fails(self, authenticated_client):
        response = authenticated_client.post(
            "/api/predict/priority/", {"text": ""}
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST