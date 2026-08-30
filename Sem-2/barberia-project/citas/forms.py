from django import forms

from .models import horarios


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
        horarios_disponibles = kwargs.pop('horarios_disponibles', horarios)
        super().__init__(*args, **kwargs)
        self.fields['horario'].choices = [
            (horario['valor'], horario['texto'])
            for horario in horarios_disponibles
        ]
