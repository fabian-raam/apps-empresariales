# Cada horario tiene un valor para el formulario, un texto visible y un barbero.
horarios = [
    {'valor': '10:00', 'texto': '10:00 a. m. - 11:00 a. m.', 'barbero': 'Barbero 1'},
    {'valor': '11:00', 'texto': '11:00 a. m. - 12:00 p. m.', 'barbero': 'Barbero 1'},
    {'valor': '12:00', 'texto': '12:00 p. m. - 1:00 p. m.', 'barbero': 'Barbero 1'},
    {'valor': '13:00', 'texto': '1:00 p. m. - 2:00 p. m.', 'barbero': 'Barbero 1'},
    {'valor': '14:00', 'texto': '2:00 p. m. - 3:00 p. m.', 'barbero': 'Barbero 2'},
    {'valor': '15:00', 'texto': '3:00 p. m. - 4:00 p. m.', 'barbero': 'Barbero 2'},
    {'valor': '16:00', 'texto': '4:00 p. m. - 5:00 p. m.', 'barbero': 'Barbero 2'},
    {'valor': '17:00', 'texto': '5:00 p. m. - 6:00 p. m.', 'barbero': 'Barbero 2'},
    {'valor': '18:00', 'texto': '6:00 p. m. - 7:00 p. m.', 'barbero': 'Barbero 3'},
    {'valor': '19:00', 'texto': '7:00 p. m. - 8:00 p. m.', 'barbero': 'Barbero 3'},
    {'valor': '20:00', 'texto': '8:00 p. m. - 9:00 p. m.', 'barbero': 'Barbero 3'},
    {'valor': '21:00', 'texto': '9:00 p. m. - 10:00 p. m.', 'barbero': 'Barbero 3'},
]

# Las citas se guardan aquí temporalmente. Se pierden al reiniciar el servidor.
citas = []


def buscar_horario(valor):
    """Devuelve los datos del horario seleccionado."""
    for horario in horarios:
        if horario['valor'] == valor:
            return horario
    return None


def horario_esta_ocupado(fecha, valor_horario):
    """Revisa si ya existe una cita en la fecha y horario indicados."""
    for cita in citas:
        if cita['fecha'] == fecha and cita['horario'] == valor_horario:
            return True
    return False
