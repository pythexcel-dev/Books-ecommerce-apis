from rest_framework.views import APIView
from .models import (
    User,
    Cart,
    Order,
    Book,
    Shop,
    Publisher,
    Stock
)
from .serializers import (
    UserSerializer,
    BookSerializer,
    OrderSerializer,
    CartSerializer,
    ShopSerializer,
    PublisherSerializer,
    StockSerializer,
    EmailSerializer,
    PasswordSerializer
)
from rest_framework.response import Response
from rest_framework import status,permissions
from django.contrib.auth import authenticate
from .permissions import IsSelfUser, IsVendorOnly
from django.shortcuts import get_object_or_404
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
        user = serializer.save()
        user.set_password(request.data['password'])
        user.save()

        return Response(
            {
                "message":"User Registered successfully",
                "status" : status.HTTP_201_CREATED
            }, 
            status=201
        )  

  
class LoginAPIView(APIView):
    
    def post(self, request):
        email_serializer = EmailSerializer(
            data={'email':request.data.get("email")}
        )
        password_serializer = PasswordSerializer(
            data={'password':request.data.get("password")}
        ) 
        email_serializer.is_valid(raise_exception=True)
        password_serializer.is_valid(raise_exception=True)
        email = email_serializer.validated_data['email']
        password = password_serializer.validated_data['password']
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
    
    permission_classes = [permissions.IsAuthenticated] 

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
    
    def put(self, request, user_id):   
        user = get_object_or_404(User, pk=user_id)
        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'message': 'User Updated Successfully',
            'staus': status.HTTP_200_OK
        }) 


class UserDataAPIView(ListAPIView):

    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    pagination_class = CustomPagination

    queryset = User.objects.all()
    serializer_class = UserSerializer      


class CreateShopAPIView(APIView):

    permission_classes = [permissions.IsAuthenticated, IsVendorOnly]

    def post(self, request):
        serializer = ShopSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'message': 'Shop Created Successfully',
            "status" : status.HTTP_201_CREATED
        })


class CreatePublisherAPIView(APIView):

    permission_classes = [permissions.IsAuthenticated, IsVendorOnly]

    def post(self, request):
        serializer = PublisherSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'message': 'Publisher Created Successfully',
            "status" : status.HTTP_201_CREATED
        })
    

class CreateBookAPIView(APIView):

    permission_classes = [permissions.IsAuthenticated, IsVendorOnly]
   
    def post(self, request):
        serializer = BookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'message': 'Book Created Successfully',
            "status" : status.HTTP_201_CREATED
        })


class BookDataAPIView(ListAPIView):
    
    permission_classes = [permissions.IsAuthenticated]
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
