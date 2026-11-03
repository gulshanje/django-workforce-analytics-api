from rest_framework import serializers

class PredictRequestSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=2000)

class PredictResponseSerializer(serializers.Serializer):
    priority = serializers.CharField()