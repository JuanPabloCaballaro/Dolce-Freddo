from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Usuario(AbstractUser):
    telefono = models.CharField(max_length=20, blank=True, null=True)
    ROL_CHOICES = (
        ('usuario', 'Usuario'),
        ('admin', 'Administrador'),
    )
    rol = models.CharField(max_length=10, choices=ROL_CHOICES, default='usuario')

    def __str__(self):
        return f"{self.username} ({self.get_rol_display()})"

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    gustos = models.CharField(max_length=255, help_text="Separar los gustos por coma")

    def __str__(self):
        return self.nombre

class Pedido(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('enviado', 'Enviado'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    ]
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE, related_name='pedidos')
    productos = models.ManyToManyField('Producto', through='PedidoProducto')
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='pendiente')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Pedido #{self.id} de {self.usuario.username}"

class PedidoProducto(models.Model):
    pedido = models.ForeignKey('Pedido', on_delete=models.CASCADE)
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} en Pedido #{self.pedido.id}"

class Envio(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_camino', 'En camino'),
        ('entregado', 'Entregado'),
    ]
    pedido = models.OneToOneField('Pedido', on_delete=models.CASCADE, related_name='envio')
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='pendiente')
    fecha_estimada = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Envío de Pedido #{self.pedido.id} - {self.estado}"

class Carrito(models.Model):
    usuario = models.OneToOneField('Usuario', on_delete=models.CASCADE, related_name='carrito')
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Carrito de {self.usuario.username}"

class CarritoProducto(models.Model):
    carrito = models.ForeignKey('Carrito', on_delete=models.CASCADE, related_name='productos')
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} en Carrito de {self.carrito.usuario.username}"
