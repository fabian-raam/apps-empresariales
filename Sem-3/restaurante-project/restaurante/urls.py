from django.urls import path
from . import views

app_name = "restaurante"

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("menu/", views.menu, name="menu"),
    path("reservas/<int:pk>/cancelar/", views.reserva_cancelar, name="reserva_cancelar"),

    # Clientes
    path("clientes/", views.cliente_lista, name="cliente_lista"),
    path("clientes/crear/", views.cliente_crear, name="cliente_crear"),
    path("clientes/<int:pk>/editar/", views.cliente_editar, name="cliente_editar"),
    path("clientes/<int:pk>/eliminar/", views.cliente_eliminar, name="cliente_eliminar"),

    # Administradores
    path("administradores/", views.administrador_lista, name="administrador_lista"),
    path("administradores/crear/", views.administrador_crear, name="administrador_crear"),
    path("administradores/<int:pk>/editar/", views.administrador_editar, name="administrador_editar"),
    path("administradores/<int:pk>/eliminar/", views.administrador_eliminar, name="administrador_eliminar"),

    # Mesas
    path("mesas/", views.mesa_lista, name="mesa_lista"),
    path("mesas/crear/", views.mesa_crear, name="mesa_crear"),
    path("mesas/<int:pk>/editar/", views.mesa_editar, name="mesa_editar"),
    path("mesas/<int:pk>/eliminar/", views.mesa_eliminar, name="mesa_eliminar"),

    # Reservas
    path("reservas/", views.reserva_lista, name="reserva_lista"),
    path("reservas/crear/", views.reserva_crear, name="reserva_crear"),
    path("reservas/<int:pk>/editar/", views.reserva_editar, name="reserva_editar"),
    path("reservas/<int:pk>/eliminar/", views.reserva_eliminar, name="reserva_eliminar"),

    # Categorías
    path("categorias/", views.categoria_lista, name="categoria_lista"),
    path("categorias/crear/", views.categoria_crear, name="categoria_crear"),
    path("categorias/<int:pk>/editar/", views.categoria_editar, name="categoria_editar"),
    path("categorias/<int:pk>/eliminar/", views.categoria_eliminar, name="categoria_eliminar"),

    # Platos
    path("platos/", views.plato_lista, name="plato_lista"),
    path("platos/crear/", views.plato_crear, name="plato_crear"),
    path("platos/<int:pk>/editar/", views.plato_editar, name="plato_editar"),
    path("platos/<int:pk>/eliminar/", views.plato_eliminar, name="plato_eliminar"),
]
