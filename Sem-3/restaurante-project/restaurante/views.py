from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PersonaForm, AdministradorForm, MesaForm, ReservaForm, CategoriaForm, PlatoForm
from .models import Cliente, Administrador, Mesa, Reserva, Categoria, Plato

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
    reservas = Reserva.objects.all().select_related('cliente__persona', 'mesa').order_by('-fecha', '-hora')
    return render(request, "restaurante/reserva_lista.html", {
        "reservas": reservas,
        "titulo": "Reservas",
        "crear_ruta": "restaurante:reserva_crear",
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
    platos = Plato.objects.all().select_related('categoria').order_by('categoria__nombre', 'nombre')
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
