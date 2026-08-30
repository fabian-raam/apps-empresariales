from django.urls import path

from . import views

app_name = 'citas'

urlpatterns = [
    path('', views.lista_citas, name='lista'),
    path('reservar/', views.mostrar_reserva, name='mostrar_reserva'),
    path('reservar/guardar/', views.reservar_cita, name='reservar'),
    path('cancelar/', views.cancelar_cita, name='cancelar'),
]
