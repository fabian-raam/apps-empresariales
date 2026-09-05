from django.contrib import admin
from .models import Persona, Cliente, Administrador, Mesa, Reserva, Categoria, Plato

admin.site.register([Persona, Cliente, Administrador, Mesa, Reserva, Categoria, Plato])
admin.site.site_header = "Administración del restaurante"
admin.site.site_title = "Restaurante"
admin.site.index_title = "Gestión del sistema"
