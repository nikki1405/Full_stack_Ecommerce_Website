from django.shortcuts import render, redirect
from django.views import View
from .models import Product, Customer, Cart, Payment, OrderPlaced  # Add this import at the top
from django.db.models import Count
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.utils.dateparse import parse_datetime
import json
import razorpay
from django.conf import settings

# Create your views here.
def home(request):
    return render(request, 'app/home.html')

def about(request):
    return render(request, 'app/about.html')

def contact(request):
    return render(request, 'app/contact.html')

class CategoryView(View):
    def get(self, request, val):
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title').annotate(total=Count('title'))
        return render(request, 'app/category.html', {'title': title, 'product': product})

class CategoryTitle(View):
    def get(self, request, val):
        product = Product.objects.filter(title=val)
        title=Product.objects.filter(category=product[0].category).values('title').annotate(total=Count('title'))
        return render(request, 'app/category.html',locals())
class ProductDetail(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        return render(request, 'app/productdetail.html',locals())
    
class CustomerRegistrationView(View):
    def get(self,request):
        form=CustomerRegistrationForm()
        return render(request,'app/customerregistration.html',locals())
    def post(self,request):
        form=CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Congratulations!! Registered Successfully')
        else:
                messages.warning(request,'Failed to Register')
        return render(request,'app/customerregistration.html',locals())
    



@login_required
def profile_view(request):
    try:
        # Try to get existing customer profile
        customer = request.user.customer
    except:
        # Create new customer profile if doesn't exist
        customer = Customer.objects.create(user=request.user)
    
    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = CustomerProfileForm(instance=customer)
    return render(request, 'app/profile.html', {'form': form})


def address(request):
    add=Customer.objects.filter(user=request.user)
    return render(request,'app/address.html',locals())

class updateAddress(View):
    def get(self, request, pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        context = {
            'form': form,
            'add': add
        }
        return render(request, 'app/updateAddress.html', context)
    
    def post(self, request, pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(request.POST, instance=add)
        if form.is_valid():
            form.save()
            messages.success(request, 'Address updated successfully!!')
        else:
            messages.warning(request, 'Failed to update address')
        return redirect('address')

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('login')

class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, "Logged out successfully!")
        return redirect('login')


@login_required
def add_to_cart(request):
    if request.method == 'POST':
        user = request.user
        product_id = request.POST.get('prod_id')
        try:
            product = Product.objects.get(id=product_id)
            Cart(user=user, product=product).save()
            messages.success(request, 'Product added to cart successfully!')
            return redirect('cart')
        except Product.DoesNotExist:
            messages.error(request, 'Product not found!')
            return redirect('home')
    return redirect('home')

@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = sum(item.product.discounted_price for item in cart)
        shipping_amount = 10.0 if amount < 500 else 0
        total_amount = amount + shipping_amount
        total_items = cart.count()
        return render(request, 'app/cart.html', {
            'cart': cart,
            'amount': amount,
            'shipping_amount': shipping_amount,
            'total_amount': total_amount,
            'total_items': total_items
        })
    return redirect('login')

@login_required
def update_cart_quantity(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        cart_item_id = data.get('item_id')
        action = data.get('action')
        
        try:
            cart_item = Cart.objects.get(id=cart_item_id, user=request.user)
            
            if action == 'increase':
                cart_item.quantity += 1
            elif action == 'decrease' and cart_item.quantity > 1:
                cart_item.quantity -= 1
                
            cart_item.save()
            
            # Recalculate cart totals
            cart = Cart.objects.filter(user=request.user)
            total_items = sum(item.quantity for item in cart)  # Calculate total items
            amount = sum(item.product.discounted_price * item.quantity for item in cart)
            shipping_amount = 10.0 if amount < 500 else 0
            total_amount = amount + shipping_amount
            
            return JsonResponse({
                'success': True,
                'quantity': cart_item.quantity,
                'item_total': cart_item.quantity * cart_item.product.discounted_price,
                'amount': amount,
                'shipping_amount': shipping_amount,
                'total_amount': total_amount,
                'total_items': total_items  # Add total items to response
            })
            
        except Cart.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Item not found'})
            
    return JsonResponse({'success': False, 'error': 'Invalid request'})

@login_required
def remove_from_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('prod_id')
        try:
            cart_item = Cart.objects.get(user=request.user, product_id=product_id)
            cart_item.delete()
            messages.success(request, 'Item removed from cart successfully!')
        except Cart.DoesNotExist:
            messages.error(request, 'Item not found in cart!')
    return redirect('cart')

@login_required
def checkout(request):
    user = request.user
    addresses = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    
    amount = sum(item.quantity * item.product.discounted_price for item in cart_items)
    shipping_amount = 10.0 if amount < 500 else 0
    total_amount = amount + shipping_amount
    
    # Initialize Razorpay client
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    
    # Create Razorpay order
    payment = client.order.create({
        'amount': int(total_amount * 100),  # Amount in paise
        'currency': 'INR',
        'payment_capture': '1'
    })
    
    order_id = payment['id']
    
    context = {
        'addresses': addresses,
        'cart_items': cart_items,
        'amount': amount,
        'shipping_amount': shipping_amount,
        'total_amount': total_amount,
        'order_id': order_id,
        'razorpay_merchant_key': settings.RAZORPAY_KEY_ID,
        'razoramount': int(total_amount * 100)
    }
    
    return render(request, 'app/checkout.html', context)

@login_required
def payment(request):
    order_id = request.GET.get('order_id')
    payment_id = request.GET.get('payment_id')
    address_id = request.GET.get('address_id')
    
    try:
        user = request.user
        address = Customer.objects.get(id=address_id)
        payment = Payment.objects.create(
            razorpay_payment_id=payment_id,
            paid=True
        )
        
        cart_items = Cart.objects.filter(user=user)
        for item in cart_items:
            OrderPlaced.objects.create(
                user=user,
                address=address,
                product=item.product,
                quantity=item.quantity,
                payment=payment,
                order_id=f"ORDER_{payment_id}_{item.id}",
                status='Pending'
            )
        
        cart_items.delete()
        messages.success(request, 'Order placed successfully!')
        return redirect('orders')
        
    except Exception as e:
        messages.error(request, f'Error processing payment: {str(e)}')
        return redirect('checkout')


@login_required
def orders(request):
    orders = OrderPlaced.objects.filter(user=request.user).order_by('-ordered_date')
    return render(request, 'app/orders.html', {
        'orders': orders
    })

@login_required
def payment_done(request):
    if request.method == 'POST':
        payment_id = request.POST.get('razorpay_payment_id')
        address_id = request.POST.get('address_id')
        
        try:
            # Create payment record
            payment = Payment.objects.create(
                razorpay_payment_id=payment_id,
                paid=True
            )
            
            # Get selected address
            address = Customer.objects.get(id=address_id)
            
            # Create orders for cart items
            cart_items = Cart.objects.filter(user=request.user)
            for item in cart_items:
                OrderPlaced.objects.create(
                    user=request.user,
                    product=item.product,
                    address=address,
                    quantity=item.quantity,
                    payment=payment,
                    order_id=f"ORDER_{payment_id}_{item.id}"
                )
            
            # Clear cart
            cart_items.delete()
            
            messages.success(request, 'Order placed successfully!')
            return redirect('orders')
            
        except Exception as e:
            messages.error(request, f'Error processing order: {str(e)}')
            return redirect('checkout')
    
    return redirect('checkout')