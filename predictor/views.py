from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import PredictRequestSerializer, PredictResponseSerializer
from .services import predict_priority

class PredictPriorityView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PredictRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            priority = predict_priority(serializer.validated_data["text"])
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        return Response(PredictResponseSerializer({"priority": priority}).data)