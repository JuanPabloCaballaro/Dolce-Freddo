from django.urls import path
from .views import *

urlpatterns = [
    # URLs de autenticación
    path('registro/', registro, name='registro'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    
    # URLs principales
    path('', home, name='home'),
    path('productos/', productos_lista, name='productos_lista'),
    path('producto/<int:pk>/', producto_detalle, name='producto_detalle'),
    
    # URLs del carrito
    path('carrito/', carrito, name='carrito'),
    path('agregar-al-carrito/', agregar_al_carrito, name='agregar_al_carrito'),
    path('actualizar-carrito/', actualizar_carrito, name='actualizar_carrito'),
    path('eliminar-del-carrito/', eliminar_del_carrito, name='eliminar_del_carrito'),
    
    # URLs de pedidos
    path('crear-pedido/', crear_pedido, name='crear_pedido'),
    path('mis-pedidos/', mis_pedidos, name='mis_pedidos'),
    path('pedido/<int:pk>/', pedido_detalle, name='pedido_detalle'),
    
    # URLs de perfil
    path('perfil/', perfil, name='perfil'),
    
    # URLs de administración
    path('admin/productos/', admin_productos, name='admin_productos'),
    path('admin/producto/crear/', admin_producto_crear, name='admin_producto_crear'),
    path('admin/producto/<int:pk>/editar/', admin_producto_editar, name='admin_producto_editar'),
    path('admin/producto/<int:pk>/eliminar/', admin_producto_eliminar, name='admin_producto_eliminar'),
    path('admin/sabores/', admin_sabores, name='admin_sabores'),
    path('admin/pedidos/', admin_pedidos, name='admin_pedidos'),
    path('admin/pedido/<int:pk>/', admin_pedido_detalle, name='admin_pedido_detalle'),
    path('admin/alertas/', admin_alertas, name='admin_alertas'),
    path('admin/promociones/', admin_promociones, name='admin_promociones'),
    path('admin/promociones/crear/', admin_promocion_crear, name='admin_promocion_crear'),
    path('admin/promociones/<int:pk>/editar/', admin_promocion_editar, name='admin_promocion_editar'),
    path('admin/promociones/<int:pk>/eliminar/', admin_promocion_eliminar, name='admin_promocion_eliminar'),

    # URLs de promociones
    path('promociones/', promociones_lista, name='promociones_lista'),
    path('promociones/<int:pk>/', promocion_detalle, name='promocion_detalle'),
]
