from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Sabor, Producto, Pedido, PedidoProducto, Envio, Carrito, CarritoProducto, Alerta, Promocion

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'email', 'telefono', 'rol', 'is_active', 'date_joined')
    list_filter = ('rol', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'telefono')
    ordering = ('-date_joined',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('Información Adicional', {'fields': ('telefono', 'rol')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información Adicional', {'fields': ('telefono', 'rol')}),
    )

@admin.register(Sabor)
class SaborAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'color', 'activo']
    list_filter = ['activo']
    search_fields = ['nombre']
    list_editable = ['activo']

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio', 'stock', 'destacado', 'activo', 'fecha_creacion')
    list_filter = ('categoria', 'destacado', 'activo', 'fecha_creacion')
    search_fields = ('nombre', 'descripcion')
    ordering = ('-fecha_creacion',)
    filter_horizontal = ('sabores',)
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion')
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'descripcion', 'categoria', 'precio', 'stock')
        }),
        ('Imagen y Sabores', {
            'fields': ('imagen', 'sabores')
        }),
        ('Estado', {
            'fields': ('destacado', 'activo')
        }),
        ('Fechas', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )

class PedidoProductoInline(admin.TabularInline):
    model = PedidoProducto
    extra = 1
    fields = ('producto', 'cantidad', 'precio_unitario', 'sabores_seleccionados')

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'estado', 'total', 'fecha')
    list_filter = ('estado', 'fecha')
    search_fields = ('usuario__username', 'usuario__email')
    ordering = ('-fecha',)
    readonly_fields = ('fecha', 'total')
    inlines = [PedidoProductoInline]
    
    fieldsets = (
        ('Información del Cliente', {
            'fields': ('usuario', 'fecha')
        }),
        ('Detalles del Pedido', {
            'fields': ('estado', 'total', 'direccion_entrega', 'telefono_entrega', 'notas')
        }),
    )

@admin.register(PedidoProducto)
class PedidoProductoAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'producto', 'cantidad', 'precio_unitario', 'subtotal')
    list_filter = ('pedido__estado',)
    search_fields = ('pedido__id', 'producto__nombre')
    readonly_fields = ('subtotal',)

@admin.register(Envio)
class EnvioAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'estado', 'direccion', 'telefono', 'fecha_estimada')
    list_filter = ('estado', 'fecha_estimada')
    search_fields = ('pedido__id', 'direccion', 'telefono')
    ordering = ('-pedido__fecha',)

@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'creado', 'actualizado', 'total_productos')
    list_filter = ('creado', 'actualizado')
    search_fields = ('usuario__username',)
    ordering = ('-actualizado',)
    
    def total_productos(self, obj):
        return obj.productos.count()
    total_productos.short_description = 'Productos en Carrito'

@admin.register(CarritoProducto)
class CarritoProductoAdmin(admin.ModelAdmin):
    list_display = ('carrito', 'producto', 'cantidad', 'subtotal', 'fecha_agregado')
    list_filter = ('fecha_agregado',)
    search_fields = ('carrito__usuario__username', 'producto__nombre')
    ordering = ('-fecha_agregado',)
    readonly_fields = ('subtotal',)

@admin.register(Alerta)
class AlertaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tipo', 'fecha_creacion', 'leida', 'activa')
    list_filter = ('tipo', 'leida', 'activa', 'fecha_creacion')
    search_fields = ('titulo', 'mensaje')
    ordering = ('-fecha_creacion',)
    readonly_fields = ('fecha_creacion',)
    
    actions = ['marcar_como_leida', 'marcar_como_no_leida']
    
    def marcar_como_leida(self, request, queryset):
        queryset.update(leida=True)
    marcar_como_leida.short_description = "Marcar como leída"
    
    def marcar_como_no_leida(self, request, queryset):
        queryset.update(leida=False)
    marcar_como_no_leida.short_description = "Marcar como no leída"

@admin.register(Promocion)
class PromocionAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'tipo', 'descuento', 'fecha_inicio', 'fecha_fin', 'esta_vigente', 'destacada', 'activa']
    list_filter = ['tipo', 'activa', 'destacada', 'fecha_inicio', 'fecha_fin']
    search_fields = ['nombre', 'descripcion']
    list_editable = ['activa', 'destacada']
    filter_horizontal = ['productos']
    date_hierarchy = 'fecha_inicio'
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'descripcion', 'tipo', 'descuento')
        }),
        ('Productos y Categorías', {
            'fields': ('productos', 'categorias')
        }),
        ('Fechas', {
            'fields': ('fecha_inicio', 'fecha_fin')
        }),
        ('Configuración', {
            'fields': ('imagen', 'activa', 'destacada')
        }),
    )
