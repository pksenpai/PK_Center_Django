from rest_framework import serializers
from .models import Order

class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['id', 'receiving_date', 'item', 'user', 'address']

    