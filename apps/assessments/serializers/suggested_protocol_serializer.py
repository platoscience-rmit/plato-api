from apps.assessments.models import SuggestedProtocol, Protocol
from rest_framework import serializers
from apps.assessments.serializers.protocol_serializer import ProtocolSerializer

class SuggestedProtocolSerializer(serializers.ModelSerializer):

    class Meta:
        model = SuggestedProtocol
        fields = [
            'id',
            'first_norm_study',
            'second_norm_study',
            'third_norm_study'
        ]

class SuggestedProtocolDetailSerializer(serializers.Serializer):
    first_protocol = ProtocolSerializer(source='get_first_protocol', read_only=True)
    second_protocol = ProtocolSerializer(source='get_second_protocol', read_only=True)
    third_protocol = ProtocolSerializer(source='get_third_protocol', read_only=True)