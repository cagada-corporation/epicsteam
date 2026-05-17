from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth import login, authenticate, logout

from django.contrib.auth.decorators import login_required

from django.http import HttpResponseForbidden

from .forms import RegisterForm, ProductForm

from .models import Product, Cart, CartItem, Category


# =========================
# 🏠 HOME
# =========================
from django.shortcuts import render
from .models import Product

def home(request):

    products = Product.objects.all()

    return render(request, 'tienda/inicio.html', {
        'products': products
    })


# =========================
# 📝 REGISTRO
# =========================
def register(request):

    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save()

            Cart.objects.create(user=user)

            login(request, user)

            return redirect('home')

    else:
        form = RegisterForm()

    return render(request, 'tienda/register.html', {
        'form': form
    })


# =========================
# 🔐 LOGIN
# =========================
def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')

        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:
            login(request, user)

            return redirect('home')

    return render(request, 'tienda/login.html')


# =========================
# 🚪 LOGOUT
# =========================
def logout_view(request):

    logout(request)

    return redirect('home')


# =========================
# 📊 DASHBOARD
# =========================
@login_required
def dashboard(request):

    if not request.user.is_seller:
        return HttpResponseForbidden("No eres vendedor")

    products = Product.objects.filter(owner=request.user)

    return render(request, 'tienda/dashboard.html', {
        'products': products
    })


# =========================
# ➕ CREAR PRODUCTO
# =========================
@login_required
def product_create(request):

    if not request.user.is_seller:
        return HttpResponseForbidden("Solo vendedores")

    form = ProductForm(
        request.POST or None,
        request.FILES or None
    )

    if form.is_valid():

        product = form.save(commit=False)

        product.owner = request.user

        product.save()

        form.save_m2m()

        return redirect('dashboard')

    return render(request, 'tienda/product_form.html', {
        'form': form
    })


# =========================
# 🛒 VER CARRITO
# =========================
@login_required
def cart_detail(request):

    cart = Cart.objects.get(user=request.user)

    return render(request, 'tienda/cart_detail.html', {
        'cart': cart
    })


# =========================
# ➕ AGREGAR AL CARRITO
# =========================
@login_required
def add_to_cart(request, product_id):

    cart = Cart.objects.get(user=request.user)

    product = get_object_or_404(Product, id=product_id)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart_detail')