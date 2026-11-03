from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Complaint
from .serializers import ComplaintSerializer

class ComplaintViewSet(viewsets.ModelViewSet):
    serializer_class = ComplaintSerializer

    def get_queryset(self):
        qs = Complaint.objects.all().order_by("-created_at")
        status_param = self.request.query_params.get("status")
        keyword = self.request.query_params.get("keyword")
        if status_param:
            qs = qs.filter(status=status_param)
        if keyword:
            qs = qs.filter(title__icontains=keyword) | qs.filter(description__icontains=keyword)
        return qs

    @action(detail=True, methods=["patch"])
    def update_status(self, request, pk=None):
        complaint = self.get_object()
        new_status = request.data.get("status")
        if new_status not in ["open", "in_progress", "closed"]:
            return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)
        complaint.status = new_status
        complaint.save()
        return Response(ComplaintSerializer(complaint).data)