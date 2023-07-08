from django.urls import path
from .views import (
    RegisterAPIView,
    LoginAPIView,
    LogoutAPIView,
    UserDataAPIView,
    UserUpdateAPIView,
    CreateBookAPIView,
    BookDataAPIView,
    StockAPIView,
    CartItemAPIView,
    CreateShopAPIView,
    CreatePublisherAPIView,
    MakeOrderAPIView
)


urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('user-data/', UserDataAPIView.as_view()),
    path('user/<int:user_id>', UserUpdateAPIView.as_view()),
    path('shop/', CreateShopAPIView.as_view()),
    path('publisher/', CreatePublisherAPIView.as_view()),
    path('book/', CreateBookAPIView.as_view()),
    path('book-data/', BookDataAPIView.as_view()),
    path('stock/', StockAPIView.as_view()),
    path('cart-item/', CartItemAPIView.as_view()),
    path('order/', MakeOrderAPIView.as_view()),
    path('logout/', LogoutAPIView.as_view()),
]