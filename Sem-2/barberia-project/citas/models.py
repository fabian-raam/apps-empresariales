from django.db import models


class Barbero(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Horario(models.Model):
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    barbero = models.ForeignKey(Barbero, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.hora_inicio:%H:%M} - {self.hora_fin:%H:%M}'


class Cita(models.Model):
    nombre_cliente = models.CharField(max_length=100)
    fecha = models.DateField()
    horario = models.ForeignKey(Horario, on_delete=models.CASCADE)

    class Meta:
        # Una fecha no puede tener dos citas en el mismo horario.
        constraints = [
            models.UniqueConstraint(
                fields=['fecha', 'horario'],
                name='cita_fecha_horario_unicos',
            )
        ]

    def __str__(self):
        return f'{self.nombre_cliente} - {self.fecha} - {self.horario}'
