from rest_framework.views import APIView
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
from .serializers import (
    UserSerializer,
    BookSerializer,
    OrderSerializer,
    ShopSerializer,
    PublisherSerializer,
    StockSerializer,
    LoginPayloadSerializer,
    CartItemSerializer,
    OrderedBookSerializer
)
from rest_framework.response import Response
from rest_framework import status,permissions
from django.contrib.auth import authenticate
from .permissions import IsSelfUser, IsVendorOnly
from django.shortcuts import get_object_or_404
from django.db.models import F, Sum
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters


class CustomPagination(PageNumberPagination):
    page_size = 3

class RegisterAPIView(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(
            {
                "message":"User Registered successfully",
                "status" : status.HTTP_201_CREATED
            }, 
            status=201
        )  

  
class LoginAPIView(APIView):
    
    def post(self, request):
        serializer = LoginPayloadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        if user := authenticate(username=email, password=password):
            token, _  = Token.objects.get_or_create(user=user)
            return Response({
                "status":status.HTTP_200_OK, 
                "massage":"User Logged in succesfully..",
                "Token": token.key
            })
        
        return Response(
            {
                "error": "Wrong Credentials",
                "status":status.HTTP_400_BAD_REQUEST,
            },
            status=400
        )


class LogoutAPIView(APIView):
    
    permission_classes = (permissions.IsAuthenticated,) 

    def post(self, request):
        user = request.user
        user.auth_token.delete()
        return Response({
                "message": "User Logout Successfully",
                "status": status.HTTP_200_OK
        })


class UserUpdateAPIView(APIView):
    
    permission_classes = [permissions.IsAuthenticated, (IsSelfUser | permissions.IsAdminUser)]
    
    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    def patch(self, request, user_id):   
        user = get_object_or_404(User, pk=user_id)
        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'message': 'User Updated Successfully',
            'staus': status.HTTP_200_OK
        }) 


class UserDataAPIView(ListAPIView):

    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)
    pagination_class = CustomPagination

    queryset = User.objects.all()
    serializer_class = UserSerializer      


class CreateShopAPIView(APIView):

    permission_classes = (permissions.IsAuthenticated, IsVendorOnly)

    def post(self, request):
        serializer = ShopSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'message': 'Shop Created Successfully',
            "status" : status.HTTP_201_CREATED
        })


class CreatePublisherAPIView(APIView):

    permission_classes = (permissions.IsAuthenticated, IsVendorOnly)

    def post(self, request):
        serializer = PublisherSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'message': 'Publisher Created Successfully',
            "status" : status.HTTP_201_CREATED
        })
    

class CreateBookAPIView(APIView):

    permission_classes = (permissions.IsAuthenticated, IsVendorOnly)
   
    def post(self, request):
        get_object_or_404(Shop, pk=request.data.get('shop'))
        serializer = BookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'message': 'Book Created Successfully',
            "status" : status.HTTP_201_CREATED
        })


class BookDataAPIView(ListAPIView):
    
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = CustomPagination
    queryset = Book.objects.filter(is_available=True)
    serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'title',
        'author',
        'description',
        'isbn',
        'publish_date',
        'is_available',
        'publisher__name',
        'shop__name',
        'price'
    ]     


class StockAPIView(APIView):

    permission_classes = (permissions.IsAuthenticated, IsVendorOnly)
   
    def post(self, request):
        book_id = request.data.get('book')
        book = get_object_or_404(Book, pk=book_id)
        request.data['shop'] = book.shop.id
        serializer = StockSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'message': 'Stock Added Successfully',
            "status" : status.HTTP_201_CREATED
        })
    

class CartItemAPIView(APIView):

    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = CustomPagination

    def get(self, request):
        user_cart = get_object_or_404(Cart, user=request.user)
        cart_items = CartItem.objects.filter(cart=user_cart, is_ordered=False)
        serializer = CartItemSerializer(cart_items, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        book_id = request.data.get('book')
        book = get_object_or_404(Book, pk=book_id)
        user = request.user

        stock = book.stock
        if stock.stock_count > 0:
            user_cart, _ = Cart.objects.get_or_create(user=user)
            cart_item, created = CartItem.objects.get_or_create(
                cart=user_cart,
                book=book,
                is_ordered=False,
                defaults={'quantity': 1}
            )
            
            if not created and cart_item.is_ordered == False:
                cart_item.quantity += 1
                cart_item.save()

            stock.stock_count -= 1
            stock.save()

            return Response({
                "message": "Book added to cart successfully!",
                "status" : status.HTTP_201_CREATED
            })
        
        return Response({
            "message": "Book is out of stock!",
            "status" : status.HTTP_204_NO_CONTENT
        })


class MakeOrderAPIView(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = request.user
        cart_items = CartItem.objects.filter(cart__user=user, is_ordered=False)

        if len(cart_items) > 0:
            total_amount = cart_items.aggregate(amount=Sum(F('book__price') * F('quantity')))['amount']
            serializer = OrderSerializer(data={
                'user':user.id,
                'total_amount': total_amount,
                'status': Order.StatusChoices.ORDERED,
                'cart': user.cart.id
            })
            serializer.is_valid(raise_exception=True)
            serializer.save()

            for item in cart_items:
                print(user.id, serializer.instance.id, item.book.id, item.quantity)
                ordered_book = OrderedBookSerializer(data={
                    'user': user.id,
                    'order': serializer.instance.id,
                    'book': item.book.id,
                    'book_quantity': item.quantity
                })

                ordered_book.is_valid(raise_exception=True)
                ordered_book.save()

            cart_items.update(is_ordered=True)

            return Response(
                {
                    "message": "Book Orderd successfully!",
                    "order_details": serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        
        return Response({
            "message": "Your Cart is Empty!",
            "status": status.HTTP_200_OK
        })
