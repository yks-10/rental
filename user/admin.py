from django.contrib import admin
from .models import User, Product, Order, OrderItem
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = ('id', 'username','name', 'email')
    list_filter = ('is_deleted', 'created_at')
    search_fields = ('unique_id', 'name', 'phone_number')

class ProductAdmin(admin.ModelAdmin):
    model = Product 
    list_display = ('id', 'product_name')
    search_fields = ('unique_id', 'product_name')

class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = ('id', 'created_at')
    list_filter = ('is_deleted', 'created_at')
    search_fields = ('unique_id', 'total_price')

class OrderItemAdmin(admin.ModelAdmin):
    model = OrderItem
    list_display = ('id', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('unique_id', )


admin.site.register(User, UserAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
