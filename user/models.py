import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, Permission, Group


# Create your models here.
class User(AbstractUser):
    unique_id = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)
    phone_number = models.CharField(null=False, max_length=10)
    name = models.CharField(verbose_name='Name', max_length=75, db_index=True, blank=False)
    email = models.EmailField(verbose_name='Email', max_length=50, blank=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    groups = models.ManyToManyField(Group, related_name='custom_users')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions')

    class Meta:
        verbose_name = 'User'
        ordering = ['-pk']

    def __str__(self):
        return str(self.name)

class Product(models.Model):
    unique_id = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)
    product_name = models.CharField(null=False, max_length=20)
    price = models.CharField(null=False, max_length=10)
    quantity = models.CharField(null=False, max_length=4)
    available = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Product'
        ordering = ['-pk']

    def __str__(self):
        return str(self.product_name)

class Order(models.Model):
    unique_id = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Order'
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

class OrderItem(models.Model):
    unique_id = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Order Item'

    def __str__(self):
        return f"Order Item {self.unique_id}"
