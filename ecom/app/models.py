from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

# Create your models here

CATEGORY_CHOICES = (
    ('CR', 'Curd'),
    ('ML', 'Milk'),
    ('BU', 'Butter'),
    ('GH', 'Ghee'),
    ('MS', 'MilkShake'),
    ('CH', 'Cheese'),
    ('YO', 'Yogurt'),
    ('LS', 'Lassi'),
    ('PA', 'Paneer'),
    ('IC', 'Ice Cream'),
    ('OT', 'Other'),
)

STATE_CHOICES = (
    ('Andaman & Nicobar Islands', 'Andaman & Nicobar Islands'),
    ('Andhra Pradesh', 'Andhra Pradesh'),
    ('Arunachal Pradesh', 'Arunachal Pradesh'),
    ('Assam', 'Assam'),
    ('Bihar', 'Bihar'),
    ('Chandigarh', 'Chandigarh'),
    ('Chhattisgarh', 'Chhattisgarh'),
    ('Dadra & Nagar Haveli and Daman & Diu', 'Dadra & Nagar Haveli and Daman & Diu'),
    ('Delhi', 'Delhi'),
    ('Goa', 'Goa'),
    ('Gujarat', 'Gujarat'),
    ('Haryana', 'Haryana'),
    ('Himachal Pradesh', 'Himachal Pradesh'),
    ('Jammu & Kashmir', 'Jammu & Kashmir'),
    ('Jharkhand', 'Jharkhand'),
    ('Karnataka', 'Karnataka'),
    ('Kerala', 'Kerala'),
    ('Ladakh', 'Ladakh'),
    ('Lakshadweep', 'Lakshadweep'),
    ('Madhya Pradesh', 'Madhya Pradesh'),
    ('Maharashtra', 'Maharashtra'),
    ('Manipur', 'Manipur'),
    ('Meghalaya', 'Meghalaya'),
    ('Mizoram', 'Mizoram'),
    ('Nagaland', 'Nagaland'),
    ('Odisha', 'Odisha'),
    ('Puducherry', 'Puducherry'),
    ('Punjab', 'Punjab'),
    ('Rajasthan', 'Rajasthan'),
    ('Sikkim', 'Sikkim'),
    ('Tamil Nadu', 'Tamil Nadu'),
    ('Telangana', 'Telangana'),
    ('Tripura', 'Tripura'),
    ('Uttar Pradesh', 'Uttar Pradesh'),
    ('Uttarakhand', 'Uttarakhand'),
    ('West Bengal', 'West Bengal'),
)

class Product(models.Model):
    title = models.CharField(max_length=255)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    composition = models.TextField()
    proadapp = models.TextField(default='')
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    Product_image = models.ImageField(upload_to='product')

    def __str__(self):
        return self.title

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    locality = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    mobile = models.CharField(max_length=10)
    zipcode = models.CharField(max_length=6)
    state = models.CharField(choices=STATE_CHOICES, max_length=50)

    def __str__(self):
        return self.name
    

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_price(self):
        return self.quantity * self.product.discounted_price

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount= models.FloatField()
    razorpay_order_id = models.CharField(max_length=255)
    razorpay_payment_status = models.CharField(max_length=255)
    razorpay_payment_id = models.CharField(max_length=255)
    paid= models.BooleanField(default=False)
    def __str__(self):
        return self.payment_id
    

class OrderPlaced(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Packed', 'Packed'),
        ('On The Way', 'On The Way'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled')
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    address = models.ForeignKey('Customer', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    payment = models.ForeignKey('Payment', on_delete=models.CASCADE)
    order_id = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ['-ordered_date']

    def __str__(self):
        return f"Order {self.order_id}"

    def get_total_cost(self):
        return self.quantity * self.product.discounted_price