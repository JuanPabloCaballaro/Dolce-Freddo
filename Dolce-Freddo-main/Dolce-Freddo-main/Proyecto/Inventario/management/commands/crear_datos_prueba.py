from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from Inventario.models import Usuario, Sabor, Producto, Alerta
from decimal import Decimal

User = get_user_model()

class Command(BaseCommand):
    help = 'Crea datos de prueba para Dolce Freddo'

    def handle(self, *args, **options):
        self.stdout.write('Creando datos de prueba...')
        
        # Crear usuario administrador
        admin_user, created = Usuario.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@dolcefreddo.com',
                'telefono': '123456789',
                'rol': 'admin',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS('Usuario administrador creado: admin/admin123'))
        
        # Crear usuario cliente
        cliente_user, created = Usuario.objects.get_or_create(
            username='cliente',
            defaults={
                'email': 'cliente@dolcefreddo.com',
                'telefono': '987654321',
                'rol': 'usuario',
            }
        )
        if created:
            cliente_user.set_password('cliente123')
            cliente_user.save()
            self.stdout.write(self.style.SUCCESS('Usuario cliente creado: cliente/cliente123'))
        
        # Crear sabores
        sabores_data = [
            {'nombre': 'Chocolate', 'descripcion': 'Chocolate negro artesanal', 'color': '#8B4513'},
            {'nombre': 'Vainilla', 'descripcion': 'Vainilla natural', 'color': '#F5DEB3'},
            {'nombre': 'Fresa', 'descripcion': 'Fresa fresca', 'color': '#FF69B4'},
            {'nombre': 'Menta', 'descripcion': 'Menta refrescante', 'color': '#98FB98'},
            {'nombre': 'Dulce de Leche', 'descripcion': 'Dulce de leche casero', 'color': '#DAA520'},
            {'nombre': 'Limón', 'descripcion': 'Limón natural', 'color': '#FFFF00'},
            {'nombre': 'Café', 'descripcion': 'Café espresso', 'color': '#8B4513'},
            {'nombre': 'Pistacho', 'descripcion': 'Pistacho tostado', 'color': '#90EE90'},
        ]
        
        sabores_creados = []
        for sabor_data in sabores_data:
            sabor, created = Sabor.objects.get_or_create(
                nombre=sabor_data['nombre'],
                defaults=sabor_data
            )
            sabores_creados.append(sabor)
            if created:
                self.stdout.write(f'Sabor creado: {sabor.nombre}')
        
        # Crear productos
        productos_data = [
            {
                'nombre': 'Helado de Chocolate',
                'descripcion': 'Helado artesanal de chocolate negro con trozos de chocolate',
                'precio': Decimal('1500.00'),
                'stock': 50,
                'categoria': 'helado',
                'destacado': True,
                'sabores': [sabores_creados[0]]  # Chocolate
            },
            {
                'nombre': 'Helado de Vainilla',
                'descripcion': 'Helado de vainilla natural con galletas',
                'precio': Decimal('1200.00'),
                'stock': 40,
                'categoria': 'helado',
                'destacado': True,
                'sabores': [sabores_creados[1]]  # Vainilla
            },
            {
                'nombre': 'Helado de Fresa',
                'descripcion': 'Helado de fresa fresca con trozos de fruta',
                'precio': Decimal('1300.00'),
                'stock': 35,
                'categoria': 'helado',
                'destacado': False,
                'sabores': [sabores_creados[2]]  # Fresa
            },
            {
                'nombre': 'Helado de Menta',
                'descripcion': 'Helado de menta refrescante con chocolate',
                'precio': Decimal('1400.00'),
                'stock': 30,
                'categoria': 'helado',
                'destacado': True,
                'sabores': [sabores_creados[3]]  # Menta
            },
            {
                'nombre': 'Helado de Dulce de Leche',
                'descripcion': 'Helado de dulce de leche casero con nueces',
                'precio': Decimal('1600.00'),
                'stock': 45,
                'categoria': 'helado',
                'destacado': True,
                'sabores': [sabores_creados[4]]  # Dulce de Leche
            },
            {
                'nombre': 'Sorbete de Limón',
                'descripcion': 'Sorbete refrescante de limón natural',
                'precio': Decimal('1000.00'),
                'stock': 25,
                'categoria': 'helado',
                'destacado': False,
                'sabores': [sabores_creados[5]]  # Limón
            },
            {
                'nombre': 'Helado de Café',
                'descripcion': 'Helado de café espresso con almendras',
                'precio': Decimal('1700.00'),
                'stock': 20,
                'categoria': 'helado',
                'destacado': False,
                'sabores': [sabores_creados[6]]  # Café
            },
            {
                'nombre': 'Helado de Pistacho',
                'descripcion': 'Helado de pistacho tostado con miel',
                'precio': Decimal('1800.00'),
                'stock': 15,
                'categoria': 'helado',
                'destacado': True,
                'sabores': [sabores_creados[7]]  # Pistacho
            },
            {
                'nombre': 'Sundae Clásico',
                'descripcion': 'Sundae con helado de vainilla, chocolate y frutillas',
                'precio': Decimal('2500.00'),
                'stock': 20,
                'categoria': 'postre',
                'destacado': True,
                'sabores': [sabores_creados[1], sabores_creados[0], sabores_creados[2]]  # Vainilla, Chocolate, Fresa
            },
            {
                'nombre': 'Banana Split',
                'descripcion': 'Banana split con tres sabores y toppings',
                'precio': Decimal('2800.00'),
                'stock': 15,
                'categoria': 'postre',
                'destacado': True,
                'sabores': [sabores_creados[1], sabores_creados[0], sabores_creados[4]]  # Vainilla, Chocolate, Dulce de Leche
            },
            {
                'nombre': 'Milkshake de Chocolate',
                'descripcion': 'Milkshake espeso de chocolate con crema',
                'precio': Decimal('2000.00'),
                'stock': 30,
                'categoria': 'bebida',
                'destacado': False,
                'sabores': [sabores_creados[0]]  # Chocolate
            },
            {
                'nombre': 'Cono Waffle',
                'descripcion': 'Cono de waffle casero para helados',
                'precio': Decimal('500.00'),
                'stock': 100,
                'categoria': 'accesorio',
                'destacado': False,
                'sabores': []
            },
        ]
        
        for producto_data in productos_data:
            sabores = producto_data.pop('sabores')
            producto, created = Producto.objects.get_or_create(
                nombre=producto_data['nombre'],
                defaults=producto_data
            )
            if created:
                producto.sabores.set(sabores)
                self.stdout.write(f'Producto creado: {producto.nombre}')
        
        # Crear alertas de ejemplo
        alertas_data = [
            {
                'titulo': 'Bienvenido a Dolce Freddo',
                'mensaje': 'Sistema de heladería online iniciado correctamente',
                'tipo': 'sistema'
            },
            {
                'titulo': 'Stock Bajo - Helado de Pistacho',
                'mensaje': 'Solo quedan 15 unidades de Helado de Pistacho',
                'tipo': 'stock'
            },
            {
                'titulo': 'Promoción Especial',
                'mensaje': '20% de descuento en todos los helados de chocolate',
                'tipo': 'promocion'
            },
            {
                'titulo': 'Nuevo Sabor Disponible',
                'mensaje': 'Ya puedes probar nuestro nuevo helado de café',
                'tipo': 'sistema'
            },
            {
                'titulo': 'Recordatorio de Inventario',
                'mensaje': 'Revisar stock de conos waffle antes del fin de semana',
                'tipo': 'stock'
            },
        ]
        
        for alerta_data in alertas_data:
            alerta, created = Alerta.objects.get_or_create(
                titulo=alerta_data['titulo'],
                defaults=alerta_data
            )
            if created:
                self.stdout.write(f'Alerta creada: {alerta.titulo}')
        
        self.stdout.write(self.style.SUCCESS('¡Datos de prueba creados exitosamente!'))
        self.stdout.write('Usuarios creados:')
        self.stdout.write('- Admin: admin/admin123')
        self.stdout.write('- Cliente: cliente/cliente123')
        self.stdout.write('Puedes acceder al admin en: http://localhost:8000/admin/') 