from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),

    # =========================
    # 🎮 DETALLE DEL PRODUCTO
    # =========================
    path(
        'product/<uuid:product_id>/',
        views.product_detail,
        name='product_detail'
    ),

    path('register/', views.register, name='register'),

    path('login/', views.login_view, name='login'),

    path('logout/', views.logout_view, name='logout'),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('products/create/', views.product_create, name='product_create'),

    path('cart/', views.cart_detail, name='cart_detail'),

    path(
        'cart/add/<uuid:product_id>/',
        views.add_to_cart,
        name='add_to_cart'
    ),

    path(
        'cart/decrease/<uuid:product_id>/',
        views.decrease_quantity,
        name='decrease_quantity'
    ),

    path(
        'cart/remove/<uuid:product_id>/',
        views.remove_from_cart,
        name='remove_from_cart'
    ),

]