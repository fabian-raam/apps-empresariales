from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

# Create your models here.
class Persona(models.Model):
    persona_id = models.BigAutoField(primary_key=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    documento = models.CharField(max_length=15, unique=True)
    telefono = models.CharField(max_length=15)
    correo = models.EmailField(unique=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"
    
class Cliente(models.Model):
    cliente_id = models.BigAutoField(primary_key=True)
    persona = models.OneToOneField(
        Persona, #Indica el modelo con q se relacion
        on_delete=models.CASCADE,#indica q si se elimina persona tmb cliente pero no alrevez
        related_name="cliente",#el nombre para marcar la relacion
    )

    def __str__(self):
        return str(self.persona)#lo q se mostrara al convertir en texto un objeto

class Administrador(models.Model):#para q identifique q es un modelo y no cualquier clase
    admin_id = models.BigAutoField(primary_key=True)
    persona = models.OneToOneField(
        Persona,
        on_delete=models.CASCADE,
        related_name="administrador",
    )
    fecha_contratacion = models.DateField()

    def __str__(self):
        return str(self.persona)

class Categoria(models.Model):
    categoria_id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)
    activa = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class Plato(models.Model):
    plato_id = models.BigAutoField(primary_key=True)
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        related_name="platos",
    )
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    img_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.nombre
    
class Mesa(models.Model):
    mesa_id = models.BigAutoField(primary_key=True)
    numero = models.PositiveIntegerField(unique=True)
    capacidad = models.PositiveIntegerField()
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return f"Mesa {self.numero}"

    def clean(self):
        super().clean()
        if self.capacidad is not None and self.capacidad < 1:
            raise ValidationError({"capacidad": "La capacidad debe ser mayor que cero."})
        if self.pk and self.capacidad is not None and self.reservas.exclude(estado="cancelada").filter(cantidad_personas__gt=self.capacidad).exists():
            raise ValidationError({"capacidad": "Existen reservas que superan esta capacidad."})

    
class Reserva(models.Model):
    ESTADOS = [
        ("pendiente", "Pendiente"),
        ("confirmada", "Confirmada"),
        ("cancelada", "Cancelada"),
    ]

    reserva_id = models.BigAutoField(primary_key=True)
    platos = models.ManyToManyField(
        Plato,
        through="DetalleReserva",
        related_name="reservas",
        blank=True,
    )

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name="reservas",
    )

    mesa = models.ForeignKey(
        Mesa,
        on_delete=models.CASCADE,
        related_name="reservas",
    )

    fecha = models.DateField()
    hora = models.TimeField()
    cantidad_personas = models.PositiveIntegerField()

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default="pendiente",
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(cantidad_personas__gt=0),
                name="reserva_cantidad_positiva",
            ), #un check de mas de 0
            models.UniqueConstraint(
                fields=["mesa", "fecha", "hora"],
                name="reserva_mesa_fecha_hora_unica",
            ), #unique de combinacion
            models.CheckConstraint(
                condition=models.Q(
                    estado__in=["pendiente", "confirmada", "cancelada"]
                ),
                name="reserva_estado_valido",
            ), #valores entre esos
        ]
    def clean(self): #reglas de negocio q no se filtran en sql
        super().clean()
        errors = {}
        if self.cantidad_personas is not None:#comprueba q existe una cantidad
            if self.cantidad_personas <= 0:
                errors["cantidad_personas"] = "La cantidad de personas debe ser mayor que cero."
                #compara q sea mayor a 0
            elif self.mesa_id and self.cantidad_personas > self.mesa.capacidad:
                errors["cantidad_personas"] = "La cantidad de personas supera la capacidad de la mesa."
                #compara q no sobrepasen el numero de mesa
        if self.mesa_id:
            anterior = None
            if self.pk:
                anterior = Reserva.objects.filter(pk=self.pk).first()
            if not self.mesa.disponible and (anterior is None or anterior.mesa_id != self.mesa_id):
                errors["mesa"] = "Seleccione una mesa disponible."
            if self.fecha and self.hora and Reserva.objects.filter(mesa_id=self.mesa_id, fecha=self.fecha, hora=self.hora).exclude(pk=self.pk).exists():
                errors["hora"] = "Esta mesa ya tiene una reserva para la fecha y hora indicadas."
        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return (
            f"Reserva de {self.cliente} - "
            f"Mesa {self.mesa.numero} - {self.fecha} {self.hora}"
        )


class FichaReserva(models.Model):
    ficha_id = models.BigAutoField(primary_key=True)
    reserva = models.OneToOneField(
        Reserva,
        on_delete=models.CASCADE,
        related_name="ficha",
    )
    ocasion = models.CharField(max_length=100, blank=True)
    observaciones = models.TextField(blank=True)

    def __str__(self):
        return f"Ficha de reserva {self.reserva_id}"


class SolicitudReserva(models.Model):
    solicitud_id = models.BigAutoField(primary_key=True)
    reserva = models.ForeignKey(
        Reserva,
        on_delete=models.CASCADE,
        related_name="solicitudes",
    )
    descripcion = models.CharField(max_length=255)
    atendida = models.BooleanField(default=False)

    def __str__(self):
        return self.descripcion


class DetalleReserva(models.Model):
    detalle_id = models.BigAutoField(primary_key=True)
    reserva = models.ForeignKey(
        Reserva,
        on_delete=models.CASCADE,
        related_name="detalles",
    )
    plato = models.ForeignKey(
        Plato,
        on_delete=models.CASCADE,
        related_name="detalles_reserva",
    )
    cantidad = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    precio_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["reserva", "plato"],
                name="detalle_reserva_plato_unico",
            ),
            models.CheckConstraint(
                condition=models.Q(cantidad__gt=0),
                name="detalle_cantidad_positiva",
            ),
            models.CheckConstraint(
                condition=models.Q(precio_unitario__gte=0),
                name="detalle_precio_no_negativo",
            ),
        ]

    def __str__(self):
        return f"{self.cantidad} x {self.plato} - Reserva {self.reserva_id}"
