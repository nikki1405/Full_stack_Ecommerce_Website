from django.contrib import admin
from .models import Product, Customer, Cart, Payment, OrderPlaced

# Register your models here.
@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id','title','discounted_price','category','Product_image']

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','name','locality','city','zipcode','state']

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
   list_display=['id','user','product','quantity']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'razorpay_payment_id', 'paid']
    list_filter = ['paid', 'razorpay_payment_status']
    search_fields = ['razorpay_order_id', 'razorpay_payment_id']

@admin.register(OrderPlaced)
class OrderPlacedAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'user', 'product', 'quantity', 'status', 'ordered_date']
    list_filter = ['status', 'ordered_date']
    search_fields = ['order_id', 'user__username']
    list_per_page = 20
    readonly_fields = ['ordered_date']
    
    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return self.readonly_fields + ['order_id', 'user', 'product', 'quantity', 'payment']
        return self.readonly_fields