import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


# =========================
# 👤 Usuario
# =========================
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    is_seller = models.BooleanField(default=False)

    def __str__(self):
        return self.username


# =========================
# 🏷️ Categoría
# =========================
class Category(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# =========================
# 🎮 Producto / Juego
# =========================
class Product(models.Model):

    PLATFORM_CHOICES = [
        ('PC', 'PC'),
        ('PS5', 'PS5'),
        ('XBOX', 'Xbox'),
        ('SWITCH', 'Nintendo Switch'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=150)

    description = models.TextField()

    image = models.ImageField(upload_to='games/')

    price = models.DecimalField(max_digits=10, decimal_places=2)

    stock = models.PositiveIntegerField(default=0)

    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='products'
    )

    categories = models.ManyToManyField(
        Category,
        related_name='products'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# =========================
# 🛒 Carrito (MODIFICADO)
# =========================
class Cart(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.OneToOneField(  # ✅ Cambiado de ForeignKey a OneToOneField
        User,
        on_delete=models.CASCADE,
        related_name='cart'  # ✅ Cambiado de 'carts' a 'cart' (singular)
    )

    products = models.ManyToManyField(
        Product,
        through='CartItem',
        related_name='carts'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total(self):
        return sum(item.subtotal for item in self.items.all())

    def __str__(self):
        return f"Cart {self.user.username}"


# =========================
# 🧾 Items del carrito
# =========================
class CartItem(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    cart = models.ForeignKey(
        Cart,
        related_name='items',
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'product')

    @property
    def subtotal(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"


# =========================
# ❤️ FAVORITOS
# =========================
class Favorite(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites'
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='favorited_by'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username} ❤️ {self.product.name}"