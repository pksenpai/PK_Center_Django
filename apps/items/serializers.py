from rest_framework import serializers
from .models import Item

class ItemSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = ['id', 'name', 'price', 'image']

    def get_image(self, item):
        first_image = item.image.first()
        if first_image:
            return first_image.src.url
        return None
    