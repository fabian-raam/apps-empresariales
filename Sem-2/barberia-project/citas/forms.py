from django import forms

from .models import Horario


class FechaForm(forms.Form):
    fecha = forms.DateField(
        label='Fecha de la cita',
        widget=forms.DateInput(attrs={'type': 'date'}),
    )


class CitaForm(forms.Form):
    nombre_cliente = forms.CharField(
        label='Nombre del cliente',
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Escribe tu nombre'}),
    )
    fecha = forms.DateField(widget=forms.HiddenInput())
    horario = forms.ChoiceField(
        label='Horario disponible',
        choices=[],
    )

    def __init__(self, *args, **kwargs):
        horarios_disponibles = kwargs.pop('horarios_disponibles', None)
        super().__init__(*args, **kwargs)

        if horarios_disponibles is None:
            horarios_disponibles = Horario.objects.all()

        self.fields['horario'].choices = [
            (horario.id, str(horario))
            for horario in horarios_disponibles
        ]
