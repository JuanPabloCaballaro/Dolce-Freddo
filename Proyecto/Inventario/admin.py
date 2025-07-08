from django.contrib import admin
from .models import Usuario, Producto, Pedido, PedidoProducto, Envio, Carrito, CarritoProducto

admin.site.register(Usuario)
admin.site.register(Producto)
admin.site.register(Pedido)
admin.site.register(PedidoProducto)
admin.site.register(Envio)
admin.site.register(Carrito)
admin.site.register(CarritoProducto)
