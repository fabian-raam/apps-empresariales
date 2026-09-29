from django.contrib import admin
from .models import (
    Persona, Cliente, Administrador, Mesa, Reserva, Categoria, Plato,
    FichaReserva, SolicitudReserva, DetalleReserva,
)


class FichaReservaInline(admin.StackedInline):
    model = FichaReserva
    fields = ("ocasion", "observaciones")
    extra = 1
    max_num = 1
    verbose_name = "ficha de la reserva"
    verbose_name_plural = "Ficha de la reserva"


class SolicitudReservaInline(admin.TabularInline):
    model = SolicitudReserva
    fields = ("descripcion", "atendida")
    extra = 1
    verbose_name_plural = "Solicitudes de la reserva"


class DetalleReservaInline(admin.TabularInline):
    model = DetalleReserva
    fields = ("plato", "cantidad", "precio_unitario")
    extra = 1
    autocomplete_fields = ("plato",)
    verbose_name_plural = "Platos de la reserva"


class PersonaAdmin(admin.ModelAdmin):
    list_display = ("persona_id", "nombres", "apellidos", "documento", "telefono", "correo")
    search_fields = ("nombres", "apellidos", "documento", "correo")
    list_filter = ("fecha_registro",)
    readonly_fields = ("fecha_registro",)


class ClienteAdmin(admin.ModelAdmin):
    list_display = ("cliente_id", "persona")
    search_fields = ("persona__nombres", "persona__apellidos", "persona__documento")
    list_select_related = ("persona",)
    autocomplete_fields = ("persona",)


class AdministradorAdmin(admin.ModelAdmin):
    list_display = ("admin_id", "persona", "fecha_contratacion")
    search_fields = ("persona__nombres", "persona__apellidos", "persona__documento")
    list_filter = ("fecha_contratacion",)
    list_select_related = ("persona",)
    autocomplete_fields = ("persona",)


class MesaAdmin(admin.ModelAdmin):
    list_display = ("mesa_id", "numero", "capacidad", "disponible")
    search_fields = ("=numero",)
    list_filter = ("disponible", "capacidad")


class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("categoria_id", "nombre", "activa")
    search_fields = ("nombre",)
    list_filter = ("activa",)


class PlatoAdmin(admin.ModelAdmin):
    list_display = ("plato_id", "nombre", "categoria", "precio", "existencias")
    search_fields = ("nombre", "categoria__nombre")
    list_filter = ("categoria",)
    list_select_related = ("categoria",)
    autocomplete_fields = ("categoria",)


class ReservaAdmin(admin.ModelAdmin):
    list_display = ("reserva_id", "cliente", "mesa", "fecha", "hora", "cantidad_personas", "estado")
    search_fields = ("cliente__persona__nombres", "cliente__persona__apellidos", "cliente__persona__documento")
    list_filter = ("estado", "fecha", "mesa")
    list_select_related = ("cliente__persona", "mesa")
    autocomplete_fields = ("cliente", "mesa")
    ordering = ("-fecha", "-hora")
    inlines = (FichaReservaInline, SolicitudReservaInline, DetalleReservaInline)


class FichaReservaAdmin(admin.ModelAdmin):
    list_display = ("ficha_id", "reserva", "ocasion", "observaciones")
    search_fields = ("ocasion", "observaciones", "reserva__cliente__persona__nombres")
    list_select_related = ("reserva__cliente__persona", "reserva__mesa")
    autocomplete_fields = ("reserva",)


class SolicitudReservaAdmin(admin.ModelAdmin):
    list_display = ("solicitud_id", "reserva", "descripcion", "atendida")
    search_fields = ("descripcion", "reserva__cliente__persona__nombres")
    list_filter = ("atendida",)
    list_select_related = ("reserva__cliente__persona", "reserva__mesa")
    autocomplete_fields = ("reserva",)


class DetalleReservaAdmin(admin.ModelAdmin):
    list_display = ("detalle_id", "reserva", "plato", "cantidad", "precio_unitario")
    search_fields = ("plato__nombre", "reserva__cliente__persona__nombres", "reserva__cliente__persona__apellidos")
    list_filter = ("plato", "reserva__estado")
    list_select_related = ("reserva__cliente__persona", "reserva__mesa", "plato")
    autocomplete_fields = ("reserva", "plato")


admin.site.register(Persona, PersonaAdmin)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Administrador, AdministradorAdmin)
admin.site.register(Mesa, MesaAdmin)
admin.site.register(Reserva, ReservaAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Plato, PlatoAdmin)
admin.site.register(FichaReserva, FichaReservaAdmin)
admin.site.register(SolicitudReserva, SolicitudReservaAdmin)
admin.site.register(DetalleReserva, DetalleReservaAdmin)
admin.site.site_header = "Administración del restaurante"
admin.site.site_title = "Restaurante"
admin.site.index_title = "Gestión del sistema"
