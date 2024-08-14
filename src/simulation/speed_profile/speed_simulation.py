import os
import pandas as pd
from geopy.distance import geodesic

# Constantes
ACCELERATION_LIMIT = 0.6  # m/s^2 (Límite de aceleración)
DECELERATION_LIMIT = -0.6  # m/s^2 (Límite de frenado)

def estimate_speed_profile(route_df):
    """
    Estima el perfil de velocidad para una ruta dada.
    
    :param route_df: DataFrame con columnas ['Latitud', 'Longitud', 'Altitud', 'Limite']
    :return: DataFrame con columna adicional 'estimated_speed', 'time_elapsed' para cada punto
    """
    n = len(route_df)
    route_df['estimated_speed'] = 0.0  # Inicializamos todas las velocidades a 0
    route_df['time_elapsed'] = 0.0     # Inicializamos todo el tiempo a 0
    
    for i in range(1, n):
        # Datos del tramo actual
        lat1, lon1 = route_df.at[i-1, 'Latitud'], route_df.at[i-1, 'Longitud']
        lat2, lon2 = route_df.at[i, 'Latitud'], route_df.at[i, 'Longitud']
        limite = route_df.at[i, 'Limite'] / 3.6  # Convertimos de km/h a m/s

        # Calculamos la distancia entre los dos puntos usando geopy
        distance = geodesic((lat1, lon1), (lat2, lon2)).meters

        # Estimamos la velocidad en el punto anterior
        prev_speed = route_df.at[i-1, 'estimated_speed']
        
        # Si es una parada (Limite = 0) o es el final de la ruta, la velocidad final debe ser 0
        if limite == 0 or i == n - 1:
            final_speed = 0.0
        else:
            final_speed = limite
        
        # Aceleración o desaceleración necesaria
        acceleration = (final_speed**2 - prev_speed**2) / (2 * distance)
        
        # Limitar la aceleración dentro de los límites legales
        if acceleration > ACCELERATION_LIMIT:
            acceleration = ACCELERATION_LIMIT
        elif acceleration < DECELERATION_LIMIT:
            acceleration = DECELERATION_LIMIT
        
        # Calcular el tiempo necesario para el tramo con la aceleración obtenida
        if acceleration != 0:
            delta_t = (final_speed - prev_speed) / acceleration
        else:
            # Caso especial cuando la aceleración es cero, implica velocidad constante
            delta_t = distance / prev_speed  # Calcula el tiempo directamente como distancia sobre velocidad
        
        # Actualizar la velocidad y el tiempo
        route_df.at[i, 'estimated_speed'] = prev_speed + acceleration * delta_t
        route_df.at[i, 'time_elapsed'] = route_df.at[i-1, 'time_elapsed'] + delta_t
    
    return route_df


# Cargamos los datos desde el CSV
route_df = pd.read_csv(os.path.join('src','simulation','speed_limits','limits','limits_linea_d2_algoritmo.csv'))  # Este CSV debería tener columnas ['Latitud', 'Longitud', 'Altitud', 'Limite']

# Calculamos el perfil de velocidad estimado
estimated_route_df = estimate_speed_profile(route_df)

# Guardamos el resultado
estimated_route_df.to_csv(os.path.join('src','simulation','speed_profile','perfil_velocidad_estimado.csv'), index=False)
