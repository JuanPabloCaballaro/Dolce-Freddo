from django.urls import path
from .views import *

urlpatterns = [
    #path('prueba/', prueba_backend, name='prueba_backend'),
    path('registro/', registro, name='registro'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('', home, name='home'),
]
