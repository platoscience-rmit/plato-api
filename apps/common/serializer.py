from rest_framework import serializers

class ErrorResponseSerializer(serializers.Serializer):
    error = serializers.CharField()

class SuccessMessageSerializer(serializers.Serializer):
    message = serializers.CharField()