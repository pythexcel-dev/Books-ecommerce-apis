from django.contrib import admin
from .models import User, Book, Cart, Order, Publisher, Shop, Stock

admin.site.register(User)
admin.site.register(Book)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Shop)
admin.site.register(Stock)
admin.site.register(Publisher)
