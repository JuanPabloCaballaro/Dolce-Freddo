# Proyecto/Inventario/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, Producto, Sabor, CarritoProducto, Pedido, Promocion

class RegistroUsuarioForm(UserCreationForm):
    telefono = forms.CharField(max_length=20, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = Usuario
        fields = ('username', 'email', 'telefono', 'password1', 'password2')

from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Usuario")
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)

class EditarPerfilForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ('email', 'telefono')

class SaborForm(forms.ModelForm):
    class Meta:
        model = Sabor
        fields = ['nombre', 'descripcion', 'color', 'activo']
        widgets = {
            'color': forms.TextInput(attrs={'type': 'color'}),
        }

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'stock', 'imagen', 'categoria', 'sabores', 'destacado', 'activo']
        widgets = {
            'precio': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'stock': forms.NumberInput(attrs={'min': '0'}),
        }

class CarritoProductoForm(forms.ModelForm):
    class Meta:
        model = CarritoProducto
        fields = ['cantidad', 'sabores_seleccionados']
        widgets = {
            'cantidad': forms.NumberInput(attrs={'min': '1', 'max': '10'}),
        }

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['direccion_entrega', 'telefono_entrega', 'notas']
        widgets = {
            'notas': forms.Textarea(attrs={'rows': 3}),
        }

class BusquedaProductoForm(forms.Form):
    q = forms.CharField(
        label='Buscar',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar productos...'
        })
    )
    categoria = forms.ChoiceField(
        label='Categoría',
        choices=[('', 'Todas las categorías')] + Producto.CATEGORIA_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    precio_min = forms.DecimalField(
        label='Precio mínimo',
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '0.00'
        })
    )
    precio_max = forms.DecimalField(
        label='Precio máximo',
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '999.99'
        })
    )

class PromocionForm(forms.ModelForm):
    class Meta:
        model = Promocion
        fields = ['nombre', 'descripcion', 'tipo', 'descuento', 'productos', 'categorias', 
                 'fecha_inicio', 'fecha_fin', 'imagen', 'activa', 'destacada']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'descuento': forms.NumberInput(attrs={'class': 'form-control'}),
            'productos': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'categorias': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'helado, postre, bebida (separadas por coma)'
            }),
            'fecha_inicio': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'fecha_fin': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'imagen': forms.FileInput(attrs={'class': 'form-control'}),
            'activa': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'destacada': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class PromocionBusquedaForm(forms.Form):
    q = forms.CharField(
        label='Buscar promociones',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar promociones...'
        })
    )
    tipo = forms.ChoiceField(
        label='Tipo de promoción',
        choices=[('', 'Todos los tipos')] + Promocion.TIPO_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    activa = forms.ChoiceField(
        label='Estado',
        choices=[
            ('', 'Todas'),
            ('vigente', 'Vigente'),
            ('expirada', 'Expirada'),
            ('futura', 'Futura')
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
