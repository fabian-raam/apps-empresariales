from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.db.models import Count, DecimalField, F, Sum
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PersonaForm, AdministradorForm, MesaForm, ReservaForm, CategoriaForm, PlatoForm, DetalleReservaForm, OperacionReservaForm
from .models import Cliente, Administrador, Mesa, Reserva, Categoria, Plato, DetalleReserva

def inicio(request):
    return render(request, "restaurante/inicio.html")


# Clientes
def cliente_lista(request):
    clientes = Cliente.objects.all().select_related('persona').order_by('persona__apellidos', 'persona__nombres')
    return render(request, "restaurante/cliente_lista.html", {
        "clientes": clientes,
        "titulo": "Clientes",
        "crear_ruta": "restaurante:cliente_crear",
    })


def cliente_crear(request):
    if request.method == "POST":
        form = PersonaForm(request.POST)
        if form.is_valid():
            persona = form.save()
            Cliente.objects.create(persona=persona)
            messages.success(request, "Cliente registrado correctamente.")
            return redirect("restaurante:cliente_lista")
    else:
        form = PersonaForm()
    return render(request, "restaurante/form.html", {
        "form": form,
        "titulo": "Clientes",
        "accion": "Registrar",
        "lista_ruta": "restaurante:cliente_lista",
    })


def cliente_editar(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == "POST":
        form = PersonaForm(request.POST, instance=cliente.persona)
        if form.is_valid():
            form.save()
            messages.success(request, "Cliente actualizado correctamente.")
            return redirect("restaurante:cliente_lista")
    else:
        form = PersonaForm(instance=cliente.persona)
    return render(request, "restaurante/form.html", {
        "form": form,
        "titulo": "Clientes",
        "accion": "Editar",
        "lista_ruta": "restaurante:cliente_lista",
    })


def cliente_eliminar(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    relacionados = cliente.reservas.select_related("cliente__persona", "mesa").all()
    if request.method == "POST":
        cliente.delete()
        messages.success(request, "Registro eliminado correctamente.")
        return redirect("restaurante:cliente_lista")
    return render(request, "restaurante/confirmar.html", {
        "objeto": cliente,
        "relacionados": relacionados,
        "accion": "Eliminar",
        "lista_ruta": "restaurante:cliente_lista",
        "conserva_persona": True,
    })


# Administradores
def administrador_lista(request):
    administradores = Administrador.objects.all().select_related('persona').order_by('persona__apellidos')
    return render(request, "restaurante/administrador_lista.html", {
        "administradores": administradores,
        "titulo": "Administradores",
        "crear_ruta": "restaurante:administrador_crear",
    })


def administrador_crear(request):
    if request.method == "POST":
        form = AdministradorForm(request.POST)
        persona_form = PersonaForm(request.POST)
        if form.is_valid() and persona_form.is_valid():
            persona = persona_form.save()
            administrador = form.save(commit=False)
            administrador.persona = persona
            administrador.save()
            messages.success(request, "Registro guardado correctamente.")
            return redirect("restaurante:administrador_lista")
    else:
        form = AdministradorForm()
        persona_form = PersonaForm()
    return render(request, "restaurante/form.html", {
        "form": form,
        "titulo": "Administradores",
        "accion": "Registrar",
        "lista_ruta": "restaurante:administrador_lista",
        "persona_form": persona_form,
    })


def administrador_editar(request, pk):
    administrador = get_object_or_404(Administrador, pk=pk)
    if request.method == "POST":
        form = AdministradorForm(request.POST, instance=administrador)
        persona_form = PersonaForm(request.POST, instance=administrador.persona)
        if form.is_valid() and persona_form.is_valid():
            persona_form.save()
            form.save()
            messages.success(request, "Registro guardado correctamente.")
            return redirect("restaurante:administrador_lista")
    else:
        form = AdministradorForm(instance=administrador)
        persona_form = PersonaForm(instance=administrador.persona)
    return render(request, "restaurante/form.html", {
        "form": form,
        "titulo": "Administradores",
        "accion": "Editar",
        "lista_ruta": "restaurante:administrador_lista",
        "persona_form": persona_form,
    })


def administrador_eliminar(request, pk):
    administrador = get_object_or_404(Administrador, pk=pk)
    if request.method == "POST":
        administrador.delete()
        messages.success(request, "Registro eliminado correctamente.")
        return redirect("restaurante:administrador_lista")
    return render(request, "restaurante/confirmar.html", {
        "objeto": administrador,
        "accion": "Eliminar",
        "lista_ruta": "restaurante:administrador_lista",
        "conserva_persona": True,
    })


# Mesas
def mesa_lista(request):
    mesas = Mesa.objects.all().order_by('numero')
    return render(request, "restaurante/mesa_lista.html", {
        "mesas": mesas,
        "titulo": "Mesas",
        "crear_ruta": "restaurante:mesa_crear",
    })


def mesa_crear(request):
    if request.method == "POST":
        form = MesaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro guardado correctamente.")
            return redirect("restaurante:mesa_lista")
    else:
        form = MesaForm()
    return render(request, "restaurante/form.html", {
        "form": form,
        "titulo": "Mesas",
        "accion": "Registrar",
        "lista_ruta": "restaurante:mesa_lista",
    })


def mesa_editar(request, pk):
    mesa = get_object_or_404(Mesa, pk=pk)
    if request.method == "POST":
        form = MesaForm(request.POST, instance=mesa)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro guardado correctamente.")
            return redirect("restaurante:mesa_lista")
    else:
        form = MesaForm(instance=mesa)
    return render(request, "restaurante/form.html", {
        "form": form,
        "titulo": "Mesas",
        "accion": "Editar",
        "lista_ruta": "restaurante:mesa_lista",
    })


def mesa_eliminar(request, pk):
    mesa = get_object_or_404(Mesa, pk=pk)
    relacionados = mesa.reservas.select_related("cliente__persona", "mesa").all()
    if request.method == "POST":
        mesa.delete()
        messages.success(request, "Registro eliminado correctamente.")
        return redirect("restaurante:mesa_lista")
    return render(request, "restaurante/confirmar.html", {
        "objeto": mesa,
        "relacionados": relacionados,
        "accion": "Eliminar",
        "lista_ruta": "restaurante:mesa_lista",
    })


# Reservas
def reserva_lista(request):
    reservas = (
        Reserva.objects.con_estado(request.GET.get("estado"))
        .del_mes_actual(request.GET.get("mes") == "actual")
        .select_related("cliente__persona", "mesa", "ficha")
        .prefetch_related("solicitudes")
        .order_by("-fecha", "-hora")
    )
    return render(request, "restaurante/reserva_lista.html", {
        "reservas": reservas,
        "titulo": "Reservas",
        "crear_ruta": "restaurante:reserva_crear",
    })


def reserva_operacion(request):
    """Guarda reserva, detalle y descuento de inventario como una unidad."""
    if request.method == "POST":
        form = OperacionReservaForm(request.POST)
        if form.is_valid():
            datos = form.cleaned_data
            try:
                with transaction.atomic():
                    actualizado = Plato.objects.filter(
                        pk=datos["plato"].pk,
                        existencias__gte=datos["cantidad"],
                    ).update(existencias=F("existencias") - datos["cantidad"])
                    if not actualizado:
                        raise ValueError("No hay existencias suficientes del plato elegido.")

                    reserva = Reserva(
                        cliente=datos["cliente"], mesa=datos["mesa"],
                        fecha=datos["fecha"], hora=datos["hora"],
                        cantidad_personas=datos["cantidad_personas"], estado="pendiente",
                    )
                    reserva.full_clean()
                    reserva.save()
                    DetalleReserva.objects.create(
                        reserva=reserva,
                        plato=datos["plato"],
                        cantidad=datos["cantidad"],
                        precio_unitario=datos["plato"].precio,
                    )
            except ValueError as error:
                form.add_error(None, str(error))
            except (ValidationError, IntegrityError) as error:
                form.add_error(None, "No se registró la operación: revise la mesa, el horario y los datos. " + str(error))
            else:
                messages.success(request, "Reserva creada y existencias actualizadas.")
                return redirect("restaurante:reserva_lista")
    else:
        form = OperacionReservaForm()
    return render(request, "restaurante/operacion_reserva.html", {"form": form})


def reporte(request):
    """Reportes agregados del restaurante con relaciones precargadas."""
    solo_mes = request.GET.get("mes") == "actual"
    base = Reserva.objects.con_estado(request.GET.get("estado")).del_mes_actual(solo_mes)
    total = DetalleReserva.objects.aggregate(
        monto_total=Sum(
            F("cantidad") * F("precio_unitario"),
            output_field=DecimalField(max_digits=14, decimal_places=2),
        ),
        unidades=Sum("cantidad"),
    )
    reservas = base.annotate(
        cantidad_detalles=Count("detalles", distinct=True),
        total_reserva=Sum(
            F("detalles__cantidad") * F("detalles__precio_unitario"),
            output_field=DecimalField(max_digits=14, decimal_places=2),
        ),
    ).select_related("cliente__persona", "mesa").prefetch_related("detalles__plato").order_by("-fecha", "-hora")
    por_estado = list(
        base.values("estado").annotate(
            reservas=Count("pk", distinct=True),
            unidades=Sum("detalles__cantidad"),
        ).order_by("-reservas", "estado")
    )
    return render(request, "restaurante/reporte.html", {
        "total": total, "reservas": reservas, "por_estado": por_estado,
    })


def reserva_crear(request):
    if request.method == "POST":
        form = ReservaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro guardado correctamente.")
            return redirect("restaurante:reserva_lista")
    else:
        form = ReservaForm()
    return render(request, "restaurante/form.html", {
        "form": form,
        "titulo": "Reservas",
        "accion": "Registrar",
        "lista_ruta": "restaurante:reserva_lista",
    })


def reserva_editar(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    if request.method == "POST":
        form = ReservaForm(request.POST, instance=reserva)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro guardado correctamente.")
            return redirect("restaurante:reserva_lista")
    else:
        form = ReservaForm(instance=reserva)
    return render(request, "restaurante/form.html", {
        "form": form,
        "titulo": "Reservas",
        "accion": "Editar",
        "lista_ruta": "restaurante:reserva_lista",
    })


def reserva_eliminar(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    if request.method == "POST":
        reserva.delete()
        messages.success(request, "Registro eliminado correctamente.")
        return redirect("restaurante:reserva_lista")
    return render(request, "restaurante/confirmar.html", {
        "objeto": reserva,
        "accion": "Eliminar",
        "lista_ruta": "restaurante:reserva_lista",
    })


# Categorías
def categoria_lista(request):
    categorias = Categoria.objects.all().order_by('nombre')
    return render(request, "restaurante/categoria_lista.html", {
        "categorias": categorias,
        "titulo": "Categorías",
        "crear_ruta": "restaurante:categoria_crear",
    })


def categoria_crear(request):
    if request.method == "POST":
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro guardado correctamente.")
            return redirect("restaurante:categoria_lista")
    else:
        form = CategoriaForm()
    return render(request, "restaurante/form.html", {
        "form": form,
        "titulo": "Categorías",
        "accion": "Registrar",
        "lista_ruta": "restaurante:categoria_lista",
    })


def categoria_editar(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == "POST":
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro guardado correctamente.")
            return redirect("restaurante:categoria_lista")
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, "restaurante/form.html", {
        "form": form,
        "titulo": "Categorías",
        "accion": "Editar",
        "lista_ruta": "restaurante:categoria_lista",
    })


def categoria_eliminar(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    relacionados = categoria.platos.all()
    if request.method == "POST":
        categoria.delete()
        messages.success(request, "Registro eliminado correctamente.")
        return redirect("restaurante:categoria_lista")
    return render(request, "restaurante/confirmar.html", {
        "objeto": categoria,
        "relacionados": relacionados,
        "accion": "Eliminar",
        "lista_ruta": "restaurante:categoria_lista",
    })


# Platos
def plato_lista(request):
    platos = (
        Plato.objects.select_related("categoria")
        .prefetch_related("detalles_reserva__reserva")
        .order_by("categoria__nombre", "nombre")
    )
    return render(request, "restaurante/plato_lista.html", {
        "platos": platos,
        "titulo": "Platos",
        "crear_ruta": "restaurante:plato_crear",
    })


def plato_crear(request):
    if request.method == "POST":
        form = PlatoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro guardado correctamente.")
            return redirect("restaurante:plato_lista")
    else:
        form = PlatoForm()
    return render(request, "restaurante/form.html", {
        "form": form,
        "titulo": "Platos",
        "accion": "Registrar",
        "lista_ruta": "restaurante:plato_lista",
    })


def plato_editar(request, pk):
    plato = get_object_or_404(Plato, pk=pk)
    if request.method == "POST":
        form = PlatoForm(request.POST, instance=plato)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro guardado correctamente.")
            return redirect("restaurante:plato_lista")
    else:
        form = PlatoForm(instance=plato)
    return render(request, "restaurante/form.html", {
        "form": form,
        "titulo": "Platos",
        "accion": "Editar",
        "lista_ruta": "restaurante:plato_lista",
    })


def plato_eliminar(request, pk):
    plato = get_object_or_404(Plato, pk=pk)
    if request.method == "POST":
        plato.delete()
        messages.success(request, "Registro eliminado correctamente.")
        return redirect("restaurante:plato_lista")
    return render(request, "restaurante/confirmar.html", {
        "objeto": plato,
        "accion": "Eliminar",
        "lista_ruta": "restaurante:plato_lista",
    })


def reserva_cancelar(request, pk):
    reserva = get_object_or_404(Reserva.objects.select_related("cliente__persona", "mesa"), pk=pk)
    if request.method == "POST":
        reserva.estado = "cancelada"
        reserva.save()
        messages.success(request, "Reserva cancelada. El registro se conserva.")
        return redirect("restaurante:reserva_lista")
    return render(request, "restaurante/confirmar.html", {"lista_ruta": "restaurante:reserva_lista", "objeto": reserva, "accion": "Cancelar reserva"})


def detalle_lista(request):
    detalles = DetalleReserva.objects.select_related(
        "reserva__cliente__persona", "reserva__mesa", "plato"
    ).order_by("-reserva__fecha", "-reserva__hora", "plato__nombre")
    return render(request, "restaurante/detalle_lista.html", {
        "detalles": detalles,
        "titulo": "Detalles de reserva",
        "crear_ruta": "restaurante:detalle_crear",
    })


def detalle_crear(request):
    if request.method == "POST":
        form = DetalleReservaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Detalle registrado correctamente.")
            return redirect("restaurante:detalle_lista")
    else:
        form = DetalleReservaForm()
    return render(request, "restaurante/form.html", {
        "form": form,
        "titulo": "Detalles de reserva",
        "accion": "Registrar",
        "lista_ruta": "restaurante:detalle_lista",
    })


def detalle_editar(request, pk):
    detalle = get_object_or_404(DetalleReserva, pk=pk)
    if request.method == "POST":
        form = DetalleReservaForm(request.POST, instance=detalle)
        if form.is_valid():
            form.save()
            messages.success(request, "Detalle actualizado correctamente.")
            return redirect("restaurante:detalle_lista")
    else:
        form = DetalleReservaForm(instance=detalle)
    return render(request, "restaurante/form.html", {
        "form": form,
        "titulo": "Detalles de reserva",
        "accion": "Editar",
        "lista_ruta": "restaurante:detalle_lista",
    })


def detalle_eliminar(request, pk):
    detalle = get_object_or_404(DetalleReserva.objects.select_related("plato"), pk=pk)
    if request.method == "POST":
        detalle.delete()
        messages.success(request, "Detalle eliminado correctamente.")
        return redirect("restaurante:detalle_lista")
    return render(request, "restaurante/confirmar.html", {
        "objeto": detalle,
        "accion": "Eliminar",
        "lista_ruta": "restaurante:detalle_lista",
    })


def menu(request):
    seleccion = request.GET.get("categoria", "")
    categorias = Categoria.objects.all().order_by("nombre")
    grupos = categorias
    if seleccion:
        if seleccion.isdecimal() and len(seleccion) < 19:
            grupos = grupos.filter(pk=int(seleccion))
        else:
            grupos = grupos.none()
    return render(request, "restaurante/menu.html", {"categorias": categorias, "grupos": grupos.prefetch_related("platos"), "seleccion": seleccion})
