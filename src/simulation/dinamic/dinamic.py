import pandas as pd
import math
from geopy.distance import geodesic

# Constantes
MAX_ACCEL = 1.5  # m/s^2
MAX_DECEL = -1.0  # m/s^2

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calcula la distancia geodésica entre dos puntos usando geopy."""
    return geodesic((lat1, lon1), (lat2, lon2)).meters

def can_decelerate(v_initial, v_final, distance):
    """Verifica si es posible frenar de v_initial a v_final en la distancia dada."""
    required_distance = (v_initial**2 - v_final**2) / (2 * abs(MAX_DECEL))
    return required_distance <= distance

def adjust_speeds(tramos, v_initial, v_final):
    """Ajusta las velocidades hacia atrás si no es posible frenar en un tramo."""
    for i in reversed(range(len(tramos) - 1)):
        d = tramos[i]['distancia']
        if not can_decelerate(v_final[i], v_initial[i+1], d):
            # Reducir v_final[i] hasta que sea posible frenar
            v_final[i] = math.sqrt(max(v_initial[i+1]**2 + 2 * MAX_DECEL * d, 0))
            # Ahora, ajustar la velocidad inicial del tramo si es necesario
            if i > 0:
                v_initial[i] = min(v_final[i], v_initial[i])

    return v_initial, v_final

def calculate_velocity_profile(tramos):
    n = len(tramos)
    v_final = [0] * n  # Inicializa todas las velocidades finales a 0
    v_initial = [0] * n  # Inicializa todas las velocidades iniciales a 0

    # Calcula velocidades iniciales y finales de forma progresiva
    for i in range(1, n):
        d = tramos[i-1]['distancia']
        v_max = min(tramos[i-1]['vel_max'], tramos[i]['vel_max'])

        # Determina la velocidad inicial y final para cada tramo
        v_f = v_max
        v_i = math.sqrt(max(v_f**2 - 2 * MAX_ACCEL * d, 0))
        
        if v_i <= v_max:
            v_final[i-1] = v_f
            v_initial[i] = v_f

    # Revisa hacia atrás para garantizar frenado
    v_initial, v_final = adjust_speeds(tramos, v_initial, v_final)

    return v_initial, v_final

def load_and_prepare_data(file_path):
    """Carga el CSV y prepara los datos necesarios para el cálculo."""
    data = pd.read_csv(file_path)
    
    # Convertir límite de velocidad de km/h a m/s
    data['Limite'] = data['Limite'] * 1000 / 3600
    
    # Calcular la distancia entre tramos consecutivos
    tramos = []
    for i in range(len(data) - 1):
        lat1, lon1, alt1 = data.iloc[i][['Latitud', 'Longitud', 'Altitud']]
        lat2, lon2, alt2 = data.iloc[i+1][['Latitud', 'Longitud', 'Altitud']]
        distancia = calculate_distance(lat1, lon1, lat2, lon2)
        tramos.append({
            'distancia': distancia,
            'vel_max': data.iloc[i]['Limite']
        })
    
    return tramos

# Ejemplo de uso
file_path = 'data\linea_d2_algoritmo_simulation.csv'  # Ruta al archivo CSV
tramos = load_and_prepare_data(file_path)
v_initial, v_final = calculate_velocity_profile(tramos)

print(f"Velocidades iniciales: {v_initial}")
print(f"Velocidades finales: {v_final}")
