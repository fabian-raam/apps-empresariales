from django import forms

from .models import (
    Administrador,
    Categoria,
    Cliente,
    DetalleReserva,
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


class DetalleReservaForm(forms.ModelForm):
    class Meta:
        model = DetalleReserva
        fields = ["reserva", "plato", "cantidad", "precio_unitario"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["reserva"].queryset = Reserva.objects.select_related(
            "cliente__persona", "mesa"
        ).order_by("-fecha", "-hora")
        self.fields["plato"].queryset = Plato.objects.order_by("nombre")


class OperacionReservaForm(forms.Form):
    """Registra una reserva y descuenta existencias del plato elegido."""
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.select_related("persona"))
    mesa = forms.ModelChoiceField(queryset=Mesa.objects.filter(disponible=True).order_by("numero"))
    fecha = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    hora = forms.TimeField(widget=forms.TimeInput(attrs={"type": "time"}))
    cantidad_personas = forms.IntegerField(min_value=1)
    plato = forms.ModelChoiceField(queryset=Plato.objects.order_by("nombre"))
    cantidad = forms.IntegerField(min_value=1, label="Cantidad de platos")

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
    existencias = forms.IntegerField(min_value=0, required=False, initial=100)

    class Meta:
        model = Plato
        fields = ["categoria", "nombre", "precio", "existencias", "img_url"]
        labels = {"categoria": "Categoría", "img_url": "URL de imagen (opcional)"}

    def clean_existencias(self):
        valor = self.cleaned_data.get("existencias")
        if valor is not None:
            return valor
        return self.instance.existencias if self.instance.pk else 100


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
