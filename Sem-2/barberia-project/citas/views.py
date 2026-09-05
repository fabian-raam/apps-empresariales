from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import CitaForm, FechaForm
from .models import Cita, Horario


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
        # QuerySets que consultan los horarios y las citas guardadas en SQLite.
        horarios_guardados = Horario.objects.select_related('barbero').all()
        citas_guardadas = Cita.objects.select_related(
            'horario__barbero'
        ).filter(fecha=fecha_seleccionada)

        horarios_ocupados = citas_guardadas.values_list(
            'horario_id', flat=True
        )

        for horario in horarios_guardados:
            estado_horarios.append({
                'valor': horario.id,
                'texto': str(horario),
                'barbero': horario.barbero.nombre,
                'ocupado': horario.id in horarios_ocupados,
            })

        for cita in citas_guardadas:
            citas_de_la_fecha.append({
                'nombre_cliente': cita.nombre_cliente,
                'fecha': cita.fecha,
                'horario': cita.horario.id,
                'horario_texto': str(cita.horario),
                'barbero': cita.horario.barbero.nombre,
            })

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

    formulario = CitaForm(
        request.POST,
        horarios_disponibles=Horario.objects.all(),
    )

    if formulario.is_valid():
        nombre = formulario.cleaned_data['nombre_cliente'].strip()
        fecha = formulario.cleaned_data['fecha']
        horario_id = formulario.cleaned_data['horario']
        horario_seleccionado = Horario.objects.filter(id=horario_id).first()

        if not nombre:
            formulario.add_error('nombre_cliente', 'Debes ingresar un nombre.')
        elif horario_seleccionado is None:
            formulario.add_error('horario', 'El horario seleccionado no existe.')
        elif Cita.objects.filter(
            fecha=fecha,
            horario=horario_seleccionado,
        ).exists():
            formulario.add_error('horario', 'Ese horario ya está ocupado.')
        else:
            # La nueva cita se guarda de forma permanente en SQLite.
            Cita.objects.create(
                nombre_cliente=nombre,
                fecha=fecha,
                horario=horario_seleccionado,
            )
            messages.success(request, 'La cita fue registrada correctamente.')
            return redirect(f'/citas/?fecha={fecha.isoformat()}')

    messages.error(request, 'Revisa los datos del formulario.')
    return mostrar_reserva(
        request,
        formulario,
        request.POST.get('fecha', ''),
    )


def mostrar_reserva(request, formulario=None, fecha_texto=None):
    if fecha_texto is None:
        fecha_texto = request.GET.get('fecha', '')

    horarios_ocupados = Cita.objects.filter(
        fecha=fecha_texto
    ).values_list('horario_id', flat=True)

    disponibles = Horario.objects.exclude(
        id__in=horarios_ocupados
    ).select_related('barbero')

    if formulario is None:
        formulario = CitaForm(
            initial={'fecha': fecha_texto},
            horarios_disponibles=disponibles,
        )

    return render(request, 'citas/reservar.html', {
        'formulario': formulario,
        'fecha_texto': fecha_texto,
        'hay_horarios': disponibles.exists(),
    })


def cancelar_cita(request):
    if request.method == 'POST':
        fecha = request.POST.get('fecha', '')
        horario = request.POST.get('horario', '')

        # Esta funcionalidad se adaptará al ORM en el ejercicio correspondiente.
        for cita in citas:
            if cita['fecha'] == fecha and cita['horario'] == horario:
                citas.remove(cita)
                messages.success(request, 'La cita fue cancelada.')
                break

        return redirect(f'/citas/?fecha={fecha}')

    return redirect('citas:lista')
