from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Category, Product, Order, OrderItem
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout

def home(request):
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    return render(request, 'food_store/home.html', {
        'categories': categories,
        'products': products
    })

def product_list(request, category_id=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_id:
        category = get_object_or_404(Category, id=category_id)
        products = products.filter(category=category)
    return render(request, 'food_store/product_list.html', {
        'category': category,
        'categories': categories,
        'products': products
    })

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id, available=True)
    return render(request, 'food_store/product_detail.html', {
        'product': product
    })

@login_required
def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        quantity = int(request.POST.get('quantity', 1))
        
        # Create or get the current order (cart)
        order, created = Order.objects.get_or_create(
            user=request.user,
            status='pending',
            defaults={'total_amount': 0}
        )
        
        # Add item to cart
        order_item, created = OrderItem.objects.get_or_create(
            order=order,
            product=product,
            defaults={'price': product.price, 'quantity': 0}
        )
        
        if not created:
            order_item.quantity += quantity
        else:
            order_item.quantity = quantity
        order_item.save()

        # Update total amount
        order.calculate_total()
            
        messages.success(request, f'Đã thêm {product.name} vào giỏ hàng')
        return redirect('food_store:product_list')

@login_required
def cart(request):
    try:
        order = Order.objects.get(user=request.user, status='pending')
        return render(request, 'food_store/cart.html', {'order': order})
    except Order.DoesNotExist:
        return render(request, 'food_store/cart.html', {'order': None})

@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'food_store/order_confirmation.html', {'order': order})

@login_required
def checkout(request):
    try:
        order = Order.objects.get(user=request.user, status='pending')
        if request.method == 'POST':
            # Process the order
            order.shipping_address = request.POST.get('shipping_address')
            order.phone = request.POST.get('phone')
            order.status = 'processing'
            order.save()
            messages.success(request, 'Đặt hàng thành công!')
            return redirect('food_store:order_confirmation', order_id=order.id)
        return render(request, 'food_store/checkout.html', {'order': order})
    except Order.DoesNotExist:
        return redirect('food_store:product_list')

def about(request):
    return render(request, 'food_store/about.html')

def contact(request):
    return render(request, 'food_store/contact.html')

@login_required
def update_cart(request, item_id):
    if request.method == 'POST':
        order_item = get_object_or_404(OrderItem, id=item_id, order__user=request.user)
        quantity = int(request.POST.get('quantity', 1))
        
        if 1 <= quantity <= 10:
            order_item.quantity = quantity
            order_item.save()
            order_item.order.calculate_total()
            
        return redirect('food_store:cart')

@login_required
def remove_from_cart(request, item_id):
    if request.method == 'POST':
        order_item = get_object_or_404(OrderItem, id=item_id, order__user=request.user)
        order = order_item.order
        order_item.delete()
        order.calculate_total()
        
        return redirect('food_store:cart')

@login_required
def my_orders(request):
    orders = Order.objects.filter(
        user=request.user,
        status__in=['processing', 'completed']
    ).order_by('-created_at')
    return render(request, 'food_store/my_orders.html', {'orders': orders})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Tự động đăng nhập sau khi đăng ký
            messages.success(request, 'Đăng ký thành công!')
            return redirect('food_store:home')
    else:
        form = UserCreationForm()
    return render(request, 'food_store/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Đăng nhập thành công!')
            # Chuyển hướng đến trang trước đó nếu có
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('food_store:home')
        else:
            messages.error(request, 'Tên đăng nhập hoặc mật khẩu không đúng.')
    return render(request, 'food_store/login.html')

def user_logout(request):
    logout(request)
    messages.success(request, 'Đã đăng xuất thành công!')
    return redirect('food_store:home')
