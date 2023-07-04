from django.urls import path
from .views import (
    RegisterAPIView,
    LoginAPIView,
    LogoutAPIView,
    UserDataAPIView,
    UserUpdateAPIView,
    CreateBookAPIView,
    BookDataAPIView,
    CreateStockAPIView,
    CreateCartItemAPIView,
    CartItemsAPIView,
    CreateShopAPIView,
    CreatePublisherAPIView,
    MakeOrderAPIView
)


urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('users/', UserDataAPIView.as_view()),
    path('update-user/<int:user_id>', UserUpdateAPIView.as_view()),
    path('createshop/', CreateShopAPIView.as_view()),
    path('createpublisher/', CreatePublisherAPIView.as_view()),
    path('createbook/', CreateBookAPIView.as_view()),
    path('books/', BookDataAPIView.as_view()),
    path('createstock/', CreateStockAPIView.as_view()),
    path('additem/', CreateCartItemAPIView.as_view()),
    path('cartitems/', CartItemsAPIView.as_view()),
    path('order/', MakeOrderAPIView.as_view()),
    path('logout/', LogoutAPIView.as_view()),
]