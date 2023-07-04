from rest_framework import serializers
from .models import (
    User,
    Cart,
    Order,
    Book,
    Shop,
    Publisher,
    Stock,
    CartItem
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart   
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'   


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book   
        fields = '__all__'


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop   
        fields = '__all__'


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher   
        fields = '__all__'    


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock   
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem   
        fields = '__all__'


class LoginPayloadSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
