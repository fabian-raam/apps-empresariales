from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import CitaForm, FechaForm
from .models import buscar_horario, citas, horario_esta_ocupado, horarios


def lista_citas(request):
    fecha_texto = request.GET.get('fecha', '')
    formulario_fecha = FechaForm(request.GET or None)
    fecha_seleccionada = None

    if formulario_fecha.is_valid():
        fecha_seleccionada = formulario_fecha.cleaned_data['fecha']
        fecha_texto = fecha_seleccionada.isoformat()

    estado_horarios = []
    citas_de_la_fecha = []

    if fecha_seleccionada:
        for horario in horarios:
            ocupado = horario_esta_ocupado(fecha_texto, horario['valor'])
            estado_horarios.append({**horario, 'ocupado': ocupado})

        for cita in citas:
            if cita['fecha'] == fecha_texto:
                citas_de_la_fecha.append(cita)

    return render(request, 'citas/lista.html', {
        'formulario_fecha': formulario_fecha,
        'fecha_seleccionada': fecha_seleccionada,
        'fecha_texto': fecha_texto,
        'estado_horarios': estado_horarios,
        'citas_de_la_fecha': citas_de_la_fecha,
    })


def reservar_cita(request):
    if request.method != 'POST':
        return redirect('citas:lista')

    fecha_texto = request.POST.get('fecha', '')
    disponibles = []
    for horario in horarios:
        if not horario_esta_ocupado(fecha_texto, horario['valor']):
            disponibles.append(horario)

    formulario = CitaForm(request.POST, horarios_disponibles=disponibles)

    if formulario.is_valid():
        nombre = formulario.cleaned_data['nombre_cliente'].strip()
        fecha = formulario.cleaned_data['fecha'].isoformat()
        horario_seleccionado = formulario.cleaned_data['horario']
        datos_horario = buscar_horario(horario_seleccionado)

        if not nombre:
            formulario.add_error('nombre_cliente', 'Debes ingresar un nombre.')
        elif datos_horario is None:
            formulario.add_error('horario', 'El horario seleccionado no existe.')
        elif horario_esta_ocupado(fecha, horario_seleccionado):
            formulario.add_error('horario', 'Ese horario ya está ocupado.')
        else:
            # El barbero se obtiene automáticamente a partir del horario.
            nueva_cita = {
                'nombre_cliente': nombre,
                'fecha': fecha,
                'horario': horario_seleccionado,
                'horario_texto': datos_horario['texto'],
                'barbero': datos_horario['barbero'],
            }
            citas.append(nueva_cita)
            messages.success(request, 'La cita fue registrada correctamente.')
            return redirect(f'/citas/?fecha={fecha}')

    messages.error(request, 'Revisa los datos del formulario.')
    return mostrar_reserva(request, formulario, fecha_texto)


def mostrar_reserva(request, formulario=None, fecha_texto=None):
    if fecha_texto is None:
        fecha_texto = request.GET.get('fecha', '')

    disponibles = []
    for horario in horarios:
        if not horario_esta_ocupado(fecha_texto, horario['valor']):
            disponibles.append(horario)

    if formulario is None:
        formulario = CitaForm(
            initial={'fecha': fecha_texto},
            horarios_disponibles=disponibles,
        )

    return render(request, 'citas/reservar.html', {
        'formulario': formulario,
        'fecha_texto': fecha_texto,
        'hay_horarios': len(disponibles) > 0,
    })


def cancelar_cita(request):
    if request.method == 'POST':
        fecha = request.POST.get('fecha', '')
        horario = request.POST.get('horario', '')

        # Al quitar la cita de la lista, el horario vuelve a estar disponible.
        for cita in citas:
            if cita['fecha'] == fecha and cita['horario'] == horario:
                citas.remove(cita)
                messages.success(request, 'La cita fue cancelada.')
                break

        return redirect(f'/citas/?fecha={fecha}')

    return redirect('citas:lista')
