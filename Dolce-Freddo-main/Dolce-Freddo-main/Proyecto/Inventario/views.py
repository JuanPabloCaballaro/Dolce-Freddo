from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from .forms import (
    RegistroUsuarioForm, LoginForm, EditarPerfilForm, 
    ProductoForm, SaborForm, CarritoProductoForm, 
    PedidoForm, BusquedaProductoForm, PromocionForm, PromocionBusquedaForm
)
from .models import (
    Usuario, Producto, Sabor, Carrito, CarritoProducto, 
    Pedido, PedidoProducto, Envio, Alerta, Promocion
)
import os
from django.conf import settings

def es_admin(user):
    return user.is_authenticated and user.rol == 'admin'

# Vistas de autenticación
def registro(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '¡Registro exitoso! Bienvenido a Dolce Freddo.')
            return redirect('home')
    else:
        form = RegistroUsuarioForm()
    return render(request, 'registro.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'¡Bienvenido de vuelta, {user.username}!')
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'Has cerrado sesión exitosamente.')
    return redirect('login')

# Vistas principales
def home(request):
    """Página principal con los últimos 10 productos y productos destacados"""
    ultimos_productos = Producto.objects.filter(activo=True).order_by('-fecha_creacion')[:10]
    productos_destacados = Producto.objects.filter(destacado=True, activo=True)[:6]
    sabores = Sabor.objects.filter(activo=True)
    
    # Filtrar promociones vigentes usando campos de fecha
    from django.utils import timezone
    ahora = timezone.now()
    promociones_vigentes = Promocion.objects.filter(
        activa=True,
        fecha_inicio__lte=ahora,
        fecha_fin__gte=ahora
    )[:3]
    
    # Cargar imágenes de sabores
    sabores_dir = os.path.join(settings.BASE_DIR, 'Inventario', 'static', 'img', 'sabores')
    sabores_imgs = []
    if os.path.exists(sabores_dir):
        for f in os.listdir(sabores_dir):
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                sabores_imgs.append(f)
    
    # Cargar imágenes de promos
    promos_dir = os.path.join(settings.BASE_DIR, 'Inventario', 'static', 'img', 'promos')
    promos_imgs = []
    if os.path.exists(promos_dir):
        for f in os.listdir(promos_dir):
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                promos_imgs.append(f)
    
    context = {
        'ultimos_productos': ultimos_productos,
        'productos_destacados': productos_destacados,
        'sabores': sabores,
        'sabores_imgs': sabores_imgs,
        'promos_imgs': promos_imgs,
        'promociones_vigentes': promociones_vigentes,
    }
    return render(request, 'index.html', context)

def productos_lista(request):
    """Lista de productos con filtros y búsqueda"""
    form = BusquedaProductoForm(request.GET)
    productos = Producto.objects.filter(activo=True)
    
    if form.is_valid():
        q = form.cleaned_data.get('q')
        categoria = form.cleaned_data.get('categoria')
        precio_min = form.cleaned_data.get('precio_min')
        precio_max = form.cleaned_data.get('precio_max')
        
        if q:
            productos = productos.filter(
                Q(nombre__icontains=q) | Q(descripcion__icontains=q)
            )
        
        if categoria:
            productos = productos.filter(categoria=categoria)
        
        if precio_min:
            productos = productos.filter(precio__gte=precio_min)
        
        if precio_max:
            productos = productos.filter(precio__lte=precio_max)
    
    # Paginación
    paginator = Paginator(productos, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'form': form,
        'categorias': Producto.CATEGORIA_CHOICES,
    }
    return render(request, 'productos_lista.html', context)

def producto_detalle(request, pk):
    """Detalle de un producto específico"""
    producto = get_object_or_404(Producto, pk=pk, activo=True)
    productos_relacionados = Producto.objects.filter(
        categoria=producto.categoria, activo=True
    ).exclude(pk=pk)[:4]
    
    context = {
        'producto': producto,
        'productos_relacionados': productos_relacionados,
    }
    return render(request, 'producto_detalle.html', context)

# Vistas del carrito
@login_required
def carrito(request):
    """Vista del carrito del usuario"""
    carrito_obj, created = Carrito.objects.get_or_create(usuario=request.user)
    productos_carrito = carrito_obj.productos.all()
    
    if request.method == 'POST':
        form = CarritoProductoForm(request.POST)
        if form.is_valid():
            producto_id = request.POST.get('producto_id')
            producto = get_object_or_404(Producto, pk=producto_id)
            
            carrito_producto, created = CarritoProducto.objects.get_or_create(
                carrito=carrito_obj,
                producto=producto,
                defaults={'cantidad': form.cleaned_data['cantidad']}
            )
            
            if not created:
                carrito_producto.cantidad += form.cleaned_data['cantidad']
                carrito_producto.save()
            
            carrito_producto.sabores_seleccionados.set(form.cleaned_data['sabores_seleccionados'])
            messages.success(request, f'{producto.nombre} agregado al carrito.')
            return redirect('carrito')
    
    context = {
        'productos_carrito': productos_carrito,
        'total_carrito': carrito_obj.calcular_total(),
    }
    return render(request, 'carrito.html', context)

@login_required
@require_POST
def agregar_al_carrito(request):
    """Agregar producto al carrito via AJAX"""
    producto_id = request.POST.get('producto_id')
    cantidad = int(request.POST.get('cantidad', 1))
    
    producto = get_object_or_404(Producto, pk=producto_id, activo=True)
    carrito_obj, created = Carrito.objects.get_or_create(usuario=request.user)
    
    carrito_producto, created = CarritoProducto.objects.get_or_create(
        carrito=carrito_obj,
        producto=producto,
        defaults={'cantidad': cantidad}
    )
    
    if not created:
        carrito_producto.cantidad += cantidad
        carrito_producto.save()
    
    return JsonResponse({
        'success': True,
        'message': f'{producto.nombre} agregado al carrito',
        'total_productos': carrito_obj.productos.count()
    })

@login_required
@require_POST
def actualizar_carrito(request):
    """Actualizar cantidad en el carrito"""
    carrito_producto_id = request.POST.get('carrito_producto_id')
    cantidad = int(request.POST.get('cantidad', 1))
    
    carrito_producto = get_object_or_404(CarritoProducto, pk=carrito_producto_id, carrito__usuario=request.user)
    
    if cantidad <= 0:
        carrito_producto.delete()
        messages.success(request, 'Producto eliminado del carrito.')
    else:
        carrito_producto.cantidad = cantidad
        carrito_producto.save()
        messages.success(request, 'Carrito actualizado.')
    
    return redirect('carrito')

@login_required
@require_POST
def eliminar_del_carrito(request):
    """Eliminar producto del carrito"""
    carrito_producto_id = request.POST.get('carrito_producto_id')
    carrito_producto = get_object_or_404(CarritoProducto, pk=carrito_producto_id, carrito__usuario=request.user)
    producto_nombre = carrito_producto.producto.nombre
    carrito_producto.delete()
    
    messages.success(request, f'{producto_nombre} eliminado del carrito.')
    return redirect('carrito')

# Vistas de pedidos
@login_required
def crear_pedido(request):
    """Crear pedido desde el carrito"""
    carrito_obj = get_object_or_404(Carrito, usuario=request.user)
    productos_carrito = carrito_obj.productos.all()
    
    if not productos_carrito.exists():
        messages.warning(request, 'Tu carrito está vacío.')
        return redirect('carrito')
    
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            # Crear pedido
            pedido = Pedido.objects.create(
                usuario=request.user,
                direccion_entrega=form.cleaned_data['direccion_entrega'],
                telefono_entrega=form.cleaned_data['telefono_entrega'],
                notas=form.cleaned_data['notas']
            )
            
            # Agregar productos al pedido
            total_pedido = 0
            for carrito_producto in productos_carrito:
                pedido_producto = PedidoProducto.objects.create(
                    pedido=pedido,
                    producto=carrito_producto.producto,
                    cantidad=carrito_producto.cantidad,
                    precio_unitario=carrito_producto.producto.precio
                )
                pedido_producto.sabores_seleccionados.set(carrito_producto.sabores_seleccionados.all())
                total_pedido += carrito_producto.subtotal
            
            pedido.total = total_pedido
            pedido.save()
            
            # Limpiar carrito
            carrito_obj.limpiar()
            
            # Crear alerta para admin
            Alerta.objects.create(
                titulo='Nuevo Pedido',
                mensaje=f'Nuevo pedido #{pedido.id} de {request.user.username} por ${pedido.total}',
                tipo='pedido'
            )
            
            messages.success(request, f'¡Pedido creado exitosamente! Número de pedido: #{pedido.id}')
            return redirect('mis_pedidos')
    else:
        form = PedidoForm(initial={
            'telefono_entrega': request.user.telefono
        })
    
    context = {
        'form': form,
        'productos_carrito': productos_carrito,
        'total_carrito': carrito_obj.calcular_total(),
    }
    return render(request, 'crear_pedido.html', context)

@login_required
def mis_pedidos(request):
    """Lista de pedidos del usuario"""
    pedidos = Pedido.objects.filter(usuario=request.user).order_by('-fecha')
    
    context = {
        'pedidos': pedidos,
    }
    return render(request, 'mis_pedidos.html', context)

@login_required
def pedido_detalle(request, pk):
    """Detalle de un pedido específico"""
    pedido = get_object_or_404(Pedido, pk=pk, usuario=request.user)
    
    context = {
        'pedido': pedido,
    }
    return render(request, 'pedido_detalle.html', context)

# Vistas de administración (solo para admins)
@login_required
@user_passes_test(es_admin)
def admin_productos(request):
    """Panel de administración de productos"""
    productos = Producto.objects.all().order_by('-fecha_creacion')
    
    # Búsqueda
    q = request.GET.get('q')
    if q:
        productos = productos.filter(
            Q(nombre__icontains=q) | Q(descripcion__icontains=q)
        )
    
    # Paginación
    paginator = Paginator(productos, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'q': q,
    }
    return render(request, 'admin/productos.html', context)

@login_required
@user_passes_test(es_admin)
def admin_producto_crear(request):
    """Crear nuevo producto"""
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save()
            messages.success(request, f'Producto "{producto.nombre}" creado exitosamente.')
            return redirect('admin_productos')
    else:
        form = ProductoForm()
    
    context = {
        'form': form,
        'titulo': 'Crear Producto',
    }
    return render(request, 'admin/producto_form.html', context)

@login_required
@user_passes_test(es_admin)
def admin_producto_editar(request, pk):
    """Editar producto existente"""
    producto = get_object_or_404(Producto, pk=pk)
    
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            producto = form.save()
            messages.success(request, f'Producto "{producto.nombre}" actualizado exitosamente.')
            return redirect('admin_productos')
    else:
        form = ProductoForm(instance=producto)
    
    context = {
        'form': form,
        'producto': producto,
        'titulo': 'Editar Producto',
    }
    return render(request, 'admin/producto_form.html', context)

@login_required
@user_passes_test(es_admin)
def admin_producto_eliminar(request, pk):
    """Eliminar producto"""
    producto = get_object_or_404(Producto, pk=pk)
    
    if request.method == 'POST':
        nombre_producto = producto.nombre
        producto.delete()
        messages.success(request, f'Producto "{nombre_producto}" eliminado exitosamente.')
        return redirect('admin_productos')
    
    context = {
        'producto': producto,
    }
    return render(request, 'admin/producto_eliminar.html', context)

@login_required
@user_passes_test(es_admin)
def admin_sabores(request):
    """Panel de administración de sabores"""
    sabores = Sabor.objects.all().order_by('nombre')
    
    if request.method == 'POST':
        form = SaborForm(request.POST)
        if form.is_valid():
            sabor = form.save()
            messages.success(request, f'Sabor "{sabor.nombre}" creado exitosamente.')
            return redirect('admin_sabores')
    else:
        form = SaborForm()
    
    context = {
        'sabores': sabores,
        'form': form,
    }
    return render(request, 'admin/sabores.html', context)

@login_required
@user_passes_test(es_admin)
def admin_pedidos(request):
    """Panel de administración de pedidos"""
    pedidos = Pedido.objects.all().order_by('-fecha')
    
    # Filtros
    estado = request.GET.get('estado')
    if estado:
        pedidos = pedidos.filter(estado=estado)
    
    # Paginación
    paginator = Paginator(pedidos, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'estado': estado,
        'estados': Pedido.ESTADO_CHOICES,
    }
    return render(request, 'admin/pedidos.html', context)

@login_required
@user_passes_test(es_admin)
def admin_pedido_detalle(request, pk):
    """Detalle de pedido para administrador"""
    pedido = get_object_or_404(Pedido, pk=pk)
    
    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        if nuevo_estado in dict(Pedido.ESTADO_CHOICES):
            pedido.estado = nuevo_estado
            pedido.save()
            messages.success(request, f'Estado del pedido #{pedido.id} actualizado a {pedido.get_estado_display()}.')
            return redirect('admin_pedidos')
    
    context = {
        'pedido': pedido,
        'estados': Pedido.ESTADO_CHOICES,
    }
    return render(request, 'admin/pedido_detalle.html', context)

@login_required
@user_passes_test(es_admin)
def admin_alertas(request):
    """Panel de alertas para administrador"""
    alertas = Alerta.objects.filter(activa=True).order_by('-fecha_creacion')
    
    # Marcar como leídas
    if request.method == 'POST':
        alerta_id = request.POST.get('alerta_id')
        if alerta_id:
            alerta = get_object_or_404(Alerta, pk=alerta_id)
            alerta.leida = True
            alerta.save()
            return JsonResponse({'success': True})
    
    context = {
        'alertas': alertas[:10],  # Solo las últimas 10
        'alertas_no_leidas': alertas.filter(leida=False).count(),
    }
    return render(request, 'admin/alertas.html', context)

@login_required
@user_passes_test(es_admin)
def admin_promociones(request):
    """Administración de promociones"""
    promociones = Promocion.objects.all().order_by('-fecha_creacion')
    
    # Filtros
    tipo = request.GET.get('tipo')
    activa = request.GET.get('activa')
    
    if tipo:
        promociones = promociones.filter(tipo=tipo)
    if activa is not None:
        promociones = promociones.filter(activa=activa == 'true')
    
    context = {
        'promociones': promociones,
        'tipos': Promocion.TIPO_CHOICES,
    }
    return render(request, 'admin_promociones.html', context)

@login_required
@user_passes_test(es_admin)
def admin_promocion_crear(request):
    """Crear nueva promoción"""
    if request.method == 'POST':
        form = PromocionForm(request.POST, request.FILES)
        if form.is_valid():
            promocion = form.save()
            messages.success(request, f'Promoción "{promocion.nombre}" creada exitosamente.')
            return redirect('admin_promociones')
    else:
        form = PromocionForm()
    
    context = {
        'form': form,
        'titulo': 'Crear Promoción',
    }
    return render(request, 'admin_promocion_form.html', context)

@login_required
@user_passes_test(es_admin)
def admin_promocion_editar(request, pk):
    """Editar promoción existente"""
    promocion = get_object_or_404(Promocion, pk=pk)
    
    if request.method == 'POST':
        form = PromocionForm(request.POST, request.FILES, instance=promocion)
        if form.is_valid():
            form.save()
            messages.success(request, f'Promoción "{promocion.nombre}" actualizada exitosamente.')
            return redirect('admin_promociones')
    else:
        form = PromocionForm(instance=promocion)
    
    context = {
        'form': form,
        'promocion': promocion,
        'titulo': 'Editar Promoción',
    }
    return render(request, 'admin_promocion_form.html', context)

@login_required
@user_passes_test(es_admin)
def admin_promocion_eliminar(request, pk):
    """Eliminar promoción"""
    promocion = get_object_or_404(Promocion, pk=pk)
    
    if request.method == 'POST':
        nombre = promocion.nombre
        promocion.delete()
        messages.success(request, f'Promoción "{nombre}" eliminada exitosamente.')
        return redirect('admin_promociones')
    
    context = {
        'promocion': promocion,
    }
    return render(request, 'admin_promocion_eliminar.html', context)

# Vistas de perfil
@login_required
def perfil(request):
    """Perfil del usuario"""
    if request.method == 'POST':
        form = EditarPerfilForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado exitosamente.')
            return redirect('perfil')
    else:
        form = EditarPerfilForm(instance=request.user)
    
    context = {
        'form': form,
    }
    return render(request, 'perfil.html', context)

def promociones_lista(request):
    """Lista de promociones con filtros y búsqueda"""
    form = PromocionBusquedaForm(request.GET)
    promociones = Promocion.objects.filter(activa=True)
    
    if form.is_valid():
        q = form.cleaned_data.get('q')
        tipo = form.cleaned_data.get('tipo')
        activa = form.cleaned_data.get('activa')
        
        if q:
            promociones = promociones.filter(
                Q(nombre__icontains=q) | Q(descripcion__icontains=q)
            )
        
        if tipo:
            promociones = promociones.filter(tipo=tipo)
        
        if activa:
            from django.utils import timezone
            ahora = timezone.now()
            if activa == 'vigente':
                promociones = promociones.filter(fecha_inicio__lte=ahora, fecha_fin__gte=ahora)
            elif activa == 'expirada':
                promociones = promociones.filter(fecha_fin__lt=ahora)
            elif activa == 'futura':
                promociones = promociones.filter(fecha_inicio__gt=ahora)
    
    # Paginación
    paginator = Paginator(promociones, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'form': form,
    }
    return render(request, 'promociones_lista.html', context)

def promocion_detalle(request, pk):
    """Detalle de una promoción específica"""
    promocion = get_object_or_404(Promocion, pk=pk, activa=True)
    productos_promocion = promocion.productos.filter(activo=True)
    
    context = {
        'promocion': promocion,
        'productos_promocion': productos_promocion,
    }
    return render(request, 'promocion_detalle.html', context)
