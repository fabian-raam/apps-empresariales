from django import forms

from .models import (
    Administrador,
    Categoria,
    Cliente,
    Mesa,
    Persona,
    Plato,
    Reserva,
)

class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = [
            "nombres",
            "apellidos",
            "documento",
            "telefono",
            "correo",
        ]

class AdministradorForm(forms.ModelForm):
    class Meta:
        model = Administrador
        fields = ["fecha_contratacion"]
        widgets = {
            "fecha_contratacion": forms.DateInput(
                format="%Y-%m-%d", attrs={"type": "date"}
            ),
        }


class MesaForm(forms.ModelForm):
    class Meta:
        model = Mesa
        fields = ["numero", "capacidad", "disponible"]


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ["nombre", "activa"]


class PlatoForm(forms.ModelForm):
    class Meta:
        model = Plato
        fields = ["categoria", "nombre", "precio", "img_url"]
        labels = {"categoria": "Categoría", "img_url": "URL de imagen (opcional)"}


class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = [
            "cliente",
            "mesa",
            "fecha",
            "hora",
            "cantidad_personas",
            "estado",
        ]
        widgets = {
            "fecha": forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
            "hora": forms.TimeInput(attrs={"type": "time"}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from django.db.models import Q
        disponibles = Q(disponible=True)
        if self.instance.pk:
            disponibles |= Q(pk=self.instance.mesa_id)
        self.fields["mesa"].queryset = Mesa.objects.filter(disponibles).order_by("numero")
        self.fields["cliente"].queryset = Cliente.objects.select_related("persona").order_by("persona__apellidos")
