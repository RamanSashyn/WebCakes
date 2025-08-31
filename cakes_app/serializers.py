from rest_framework import serializers


class PromoCodeSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=20)