from rest_framework import serializers
from .models import (
    User,
    Cart,
    Order,
    Book,
    Shop,
    Publisher,
    Stock,
    CartItem,
    OrderedBook
)


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart   
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['user', 'total_amount', 'status', 'cart']
        extra_kwargs = {
            'user': {'write_only': True},
            'cart': {'write_only': True}
        }
  

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


class OrderedBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderedBook  
        fields = '__all__'