from django.db import models
from django.contrib.auth.models import User
from products.models import Product

class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="acc_profile"
    )
    phone = models.CharField(max_length=20, blank=True, null=True)
    newsletter_subscribed = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    crop_x = models.FloatField(default=0)
    crop_y = models.FloatField(default=0)
    crop_w = models.FloatField(default=0)
    crop_h = models.FloatField(default=0)
    
    def __str__(self):
        return f"{self.user.username} Account Profile"
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_orders")
    order_no = models.CharField(max_length=50, unique=True, verbose_name="Order Number")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Order Date")
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total Amount")
    status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Delivered', 'Delivered'),
        ('Canceled', 'Canceled')
    ], default='Pending')

    def __str__(self):
        return self.order_no
    
class Product(models.Model):
    name = models.CharField(max_length=200)
    old_price = models.DecimalField(max_digits=10, decimal_places=2)
    new_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.CharField(max_length=50, default="In Stock")

    def __str__(self):
        return self.name

class Favourite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favourites")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="favourites")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "product") 
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"