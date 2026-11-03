from rest_framework import serializers
from .models import Complaint
from predictor.services import predict_priority

class ComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = [
            "id", "employee_id", "title", "description",
            "status", "priority", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
        
    def create(self, validated_data):
        if not validated_data.get("priority"):
            text = f"{validated_data.get('title', '')} {validated_data.get('description', '')}"
            try:
                validated_data["priority"] = predict_priority(text)
            except Exception:
                validated_data["priority"] = "medium"
        return super().create(validated_data)