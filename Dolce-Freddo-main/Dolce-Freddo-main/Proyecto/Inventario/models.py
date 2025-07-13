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

class Sabor(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#000000', help_text="Color en formato hexadecimal")
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nombre

class Producto(models.Model):
    CATEGORIA_CHOICES = [
        ('helado', 'Helado'),
        ('postre', 'Postre'),
        ('bebida', 'Bebida'),
        ('accesorio', 'Accesorio'),
    ]
    
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES, default='helado')
    sabores = models.ManyToManyField(Sabor, blank=True, related_name='productos')
    destacado = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre
    
    class Meta:
        ordering = ['-fecha_creacion']

class Promocion(models.Model):
    TIPO_CHOICES = [
        ('porcentaje', 'Porcentaje'),
        ('monto_fijo', 'Monto Fijo'),
        ('2x1', '2x1'),
        ('3x2', '3x2'),
    ]
    
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    descuento = models.DecimalField(max_digits=5, decimal_places=2, help_text="Porcentaje o monto de descuento")
    productos = models.ManyToManyField(Producto, blank=True, related_name='promociones')
    categorias = models.CharField(max_length=200, blank=True, help_text="Categorías aplicables (separadas por coma)")
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    imagen = models.ImageField(upload_to='promociones/', blank=True, null=True)
    activa = models.BooleanField(default=True)
    destacada = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nombre
    
    @property
    def esta_vigente(self):
        from django.utils import timezone
        ahora = timezone.now()
        return self.activa and self.fecha_inicio <= ahora <= self.fecha_fin
    
    @property
    def dias_restantes(self):
        from django.utils import timezone
        ahora = timezone.now()
        if self.fecha_fin > ahora:
            return (self.fecha_fin - ahora).days
        return 0
    
    class Meta:
        ordering = ['-fecha_creacion']

class Pedido(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('confirmado', 'Confirmado'),
        ('en_preparacion', 'En Preparación'),
        ('enviado', 'Enviado'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    ]
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE, related_name='pedidos')
    productos = models.ManyToManyField('Producto', through='PedidoProducto')
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='pendiente')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    direccion_entrega = models.CharField(max_length=255, blank=True)
    telefono_entrega = models.CharField(max_length=20, blank=True)
    notas = models.TextField(blank=True)

    def __str__(self):
        return f"Pedido #{self.id} de {self.usuario.username}"

    def calcular_total(self):
        total = sum(item.subtotal for item in self.pedidoproducto_set.all())
        self.total = total
        self.save()
        return total

class PedidoProducto(models.Model):
    pedido = models.ForeignKey('Pedido', on_delete=models.CASCADE)
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    sabores_seleccionados = models.ManyToManyField(Sabor, blank=True)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} en Pedido #{self.pedido.id}"
    
    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario

class Envio(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_camino', 'En camino'),
        ('entregado', 'Entregado'),
        ('fallido', 'Fallido'),
    ]
    pedido = models.OneToOneField('Pedido', on_delete=models.CASCADE, related_name='envio')
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='pendiente')
    fecha_estimada = models.DateField(null=True, blank=True)
    fecha_entrega = models.DateTimeField(null=True, blank=True)
    notas_repartidor = models.TextField(blank=True)

    def __str__(self):
        return f"Envío de Pedido #{self.pedido.id} - {self.estado}"

class Carrito(models.Model):
    usuario = models.OneToOneField('Usuario', on_delete=models.CASCADE, related_name='carrito')
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Carrito de {self.usuario.username}"
    
    def calcular_total(self):
        return sum(item.subtotal for item in self.productos.all())
    
    def limpiar(self):
        self.productos.all().delete()

class CarritoProducto(models.Model):
    carrito = models.ForeignKey('Carrito', on_delete=models.CASCADE, related_name='productos')
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    sabores_seleccionados = models.ManyToManyField(Sabor, blank=True)
    fecha_agregado = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} en Carrito de {self.carrito.usuario.username}"
    
    @property
    def subtotal(self):
        return self.cantidad * self.producto.precio

class Alerta(models.Model):
    TIPO_CHOICES = [
        ('stock', 'Stock Bajo'),
        ('pedido', 'Nuevo Pedido'),
        ('envio', 'Envío'),
        ('sistema', 'Sistema'),
        ('promocion', 'Promoción'),
    ]
    
    titulo = models.CharField(max_length=200)
    mensaje = models.TextField()
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    leida = models.BooleanField(default=False)
    activa = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.titulo} - {self.get_tipo_display()}"
    
    class Meta:
        ordering = ['-fecha_creacion']
