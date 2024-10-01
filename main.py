import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import date2num
from datetime import datetime, timedelta

# Datos de las actividades
data = {
    'Actividad': [
        'Recopilar información', 'Estudiar Factibilidad', 'Preparar informe de definición del problema',
        'Entrevistar a usuarios', 'Estudiar el sistema existente', 'Definir los requisitos del usuario',
        'Preparar informe del análisis del sistema', 'Entradas y salidas', 'Procesamiento y base de datos',
        'Evaluación', 'Preparar informe del diseño del sistema', 'Programación de computación',
        'Paquetes de programas de computación', 'Red', 'Preparar informe del desarrollo del sistema',
        'Programas de computación', 'Equipos de computación', 'Red', 'Preparar informe', 'Capacitación',
        'Conversión del sistema', 'Preparar informe'
    ],
    'Duración (días)': [
        3, 4, 1, 5, 8, 5, 1, 8, 10, 2, 2, 15, 10, 6, 2, 6, 4, 4, 1, 4, 2, 1
    ],
    'Predecesoras': [
        '', '', '1, 2', '3', '3', '4', '5, 7', '7', '7', '8, 9', '10', '11', '11', '11', '12, 13, 14', '15', '15', '15', '16, 17, 18', '19', '19', '20, 21'
    ]
}

# Convertir a DataFrame
df = pd.DataFrame(data)

# Inicializar la lista de fechas de inicio
start_dates = []

# Definir las fechas de inicio basadas en las predecesoras
for i in range(len(df)):
    if df['Predecesoras'][i] == '':
        if i == 0:
            start_dates.append(datetime.today())
        else:
            start_dates.append(start_dates[i-1] + timedelta(days=int(df['Duración (días)'][i-1])))
    else:
        predecessors = [int(p) - 1 for p in df['Predecesoras'][i].split(',')]  # Convertir las predecesoras
        # Filtrar los predecesores que estén dentro del rango válido
        valid_predecessors = [p for p in predecessors if 0 <= p < len(start_dates)]
        if valid_predecessors:  # Verificar que la lista no esté vacía
            max_predecessor_end = max([start_dates[p] + timedelta(days=int(df['Duración (días)'][p])) for p in valid_predecessors])
            start_dates.append(max_predecessor_end)
        else:
            # Si no hay predecesores válidos, usar la fecha de inicio anterior
            start_dates.append(start_dates[i-1] + timedelta(days=int(df['Duración (días)'][i-1])))


# Agregar la columna de fechas de inicio y fin al DataFrame
df['Fecha de Inicio'] = start_dates
df['Fecha de Fin'] = df['Fecha de Inicio'] + pd.to_timedelta(df['Duración (días)'], unit='D')

# Crear el diagrama de Gantt
fig, ax = plt.subplots(figsize=(10, 8))

# Graficar cada actividad como una barra
for i, row in df.iterrows():
    ax.barh(row['Actividad'], date2num(row['Fecha de Fin']) - date2num(row['Fecha de Inicio']),
            left=date2num(row['Fecha de Inicio']), color='skyblue')

# Formato del eje x para mostrar las fechas
ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
plt.xticks(rotation=45)

# Etiquetas y título
plt.xlabel('Fecha')
plt.ylabel('Actividades')
plt.title('Diagrama de Gantt del Proyecto')

plt.tight_layout()
plt.show()
