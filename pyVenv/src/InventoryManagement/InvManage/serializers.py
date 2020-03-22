from rest_framework import serializers

from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name','category','quantity','identifier','location')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return data