from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegistroUsuarioForm, LoginForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.

#def prueba_backend(request):
    # Crear usuario de prueba
    # This part of the code was not provided in the original file,
    # so it will be removed to avoid errors.
    # from django.contrib.auth import get_user_model
    # User = get_user_model()
    # usuario, _ = User.objects.get_or_create(username='cliente', defaults={'telefono': '123456789', 'rol': 'usuario'})
    # usuario.set_password('test1234')
    # usuario.save()

    # Crear producto de prueba
    # This part of the code was not provided in the original file,
    # so it will be removed to avoid errors.
    # from .models import Usuario, Producto, Carrito, CarritoProducto, Pedido, PedidoProducto, Envio
    # producto, _ = Producto.objects.get_or_create(nombre='Helado Chocolate', defaults={
    #     'descripcion': 'Helado artesanal de chocolate',
    #     'precio': 1500,
    #     'stock': 10,
    #     'gustos': 'chocolate',
    # })

    # Crear carrito y agregar producto
    # This part of the code was not provided in the original file,
    # so it will be removed to avoid errors.
    # carrito, _ = Carrito.objects.get_or_create(usuario=usuario)
    # cp, _ = CarritoProducto.objects.get_or_create(carrito=carrito, producto=producto, defaults={'cantidad': 2})

    # Confirmar pedido desde el carrito
    # This part of the code was not provided in the original file,
    # so it will be removed to avoid errors.
    # pedido = Pedido.objects.create(usuario=usuario, total=producto.precio * cp.cantidad)
    # PedidoProducto.objects.create(pedido=pedido, producto=producto, cantidad=cp.cantidad)

    # Crear envío
    # This part of the code was not provided in the original file,
    # so it will be removed to avoid errors.
    # Envio.objects.create(pedido=pedido, direccion='Calle Falsa 123', telefono=usuario.telefono)

    #return render(request, 'prueba_backend.html') # Changed to render a template

def registro(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Cambia 'home' por la vista que desees
    else:
        form = RegistroUsuarioForm()
    return render(request, 'registro.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirige al index
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

#@login_required
def home(request):
    return render(request, 'index.html')
