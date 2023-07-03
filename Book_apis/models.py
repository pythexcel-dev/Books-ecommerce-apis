from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):

    USER_ROLES = [
        ('ADMIN', 'Admin'),
        ('CUSTOMER', 'Customer'),
        ('VENDOR', 'Vendor')
    ]
    created_at = models.DateTimeField(auto_now_add=True)
    date_of_birth = models.DateField(null=True)
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=350)
    last_name = models.CharField(max_length=350)
    phone = models.CharField(max_length=350, null=True, unique=True)
    username = models.CharField(max_length=350, null=True)
    user_role = models.CharField(
        max_length=20,
        choices=USER_ROLES,
        default='CUSTOMER'
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def __str__(self):
        return self.email
    

class Publisher(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()

    def __str__(self):
        return self.name


class Shop(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    
    def __str__(self):
        return self.name   
    

class Book(models.Model):
    
    title = models.CharField(max_length=100)
    isbn = models.CharField(max_length=250, unique=True)
    description = models.CharField(max_length=500)
    publish_date = models.DateField(auto_now_add=True)
    is_available = models.BooleanField(default=True)
    price=models.IntegerField()
    author = models.CharField(max_length=250)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title
    

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return f"Cart for {self.user}"
    

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    odered_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.IntegerField()
    status = models.CharField(max_length=100, choices=STATUS_CHOICES)

    def __str__(self):
        return f"Order by {self.user}"


class Stock(models.Model):
    shop = models.OneToOneField(Shop, on_delete=models.CASCADE)
    book = models.OneToOneField(Book, on_delete=models.CASCADE)
    stock_count = models.IntegerField(default=0)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"CartItem: {self.book.title} in Cart of : {self.cart.user.email}"
