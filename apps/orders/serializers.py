from rest_framework import serializers
from .models import Order


class ShowPaymentSerializer(serializers.Serializer):
    price = serializers.DecimalField(required=True, min_value=0, max_digits=1000, decimal_places=2)
    count = serializers.IntegerField(required=True, min_value=0)


class FinalizePaymentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Order
        fields = '__all__'

        