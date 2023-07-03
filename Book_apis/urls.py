from django.urls import path
from .views import (
    RegisterAPIView,
    LoginAPIView,
    LogoutAPIView,
    UserDataAPIView,
    UserUpdateAPIView,
    CreateBookAPIView,
    BookDataAPIView,
    #CreateCartItemAPIView,
    #CartDataAPIView,
    CreateShopAPIView,
    CreatePublisherAPIView
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
    #path('createcart/', CreateCartItemAPIView.as_view()),
    #path('cartitems/', CartDataAPIView.as_view()),
    path('logout/', LogoutAPIView.as_view()),
]