from rest_framework import serializers
from apps.users.models import Account

class AccountSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    class Meta:
        model = Account
        fields = '__all__'