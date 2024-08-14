import pandas as pd
from geopy.distance import geodesic

def load_data(filepath):
    """Carga los datos del CSV."""
    return pd.read_csv(filepath)

def calculate_speed_and_time(df, max_acceleration):
    """Calcula las velocidades y tiempos acumulados para cada tramo."""
    # Inicializar variables
    initial_speed = 0
    cumulative_time = 0

    # Listas para almacenar resultados
    velocities = []
    cumulative_times = []

    for i in range(len(df) - 1):
        coord1 = (df.loc[i, 'Latitud'], df.loc[i, 'Longitud'])
        coord2 = (df.loc[i+1, 'Latitud'], df.loc[i+1, 'Longitud'])
        dist = geodesic(coord1, coord2).meters
        limit = df.loc[i+1, 'Limite']
        
        accel, decel = 0, 0
        
        if limit == 0:
            final_speed = 0
            required_deceleration = (initial_speed**2) / (2 * dist)
            decel = min(max_acceleration, required_deceleration)
        elif limit < initial_speed:
            required_deceleration = (initial_speed**2 - limit**2) / (2 * dist)
            decel = min(max_acceleration, required_deceleration)
            final_speed = limit
        elif limit > initial_speed:
            required_acceleration = (limit**2 - initial_speed**2) / (2 * dist)
            accel = min(max_acceleration, required_acceleration)
            final_speed = limit
        else:
            final_speed = limit

        if decel > 0:
            time = (initial_speed - final_speed) / decel
        elif accel > 0:
            time = (final_speed - initial_speed) / accel
        else:
            time = dist / max(initial_speed, 0.1)

        cumulative_time += time
        avg_speed = (initial_speed + final_speed) / 2
        velocities.append(avg_speed)
        cumulative_times.append(cumulative_time)
        
        initial_speed = final_speed

    return velocities, cumulative_times

def save_results(df, velocities, cumulative_times, output_filepath):
    """Guarda los resultados en un CSV."""
    df['simulated_speed'] = [0] + velocities
    df['cumulative_time'] = [0] + cumulative_times
    df.to_csv(output_filepath, index=False)

def main():
    # Parámetros
    input_filepath = 'data/linea_d2_algoritmo_simulation.csv'
    output_filepath = 'src/simulation/speed_profile/perfil_velocidad_estimado.csv'
    max_acceleration = 0.6

    # Cargar los datos
    df = load_data(input_filepath)
    
    # Calcular velocidades y tiempos
    velocities, cumulative_times = calculate_speed_and_time(df, max_acceleration)
    
    # Guardar resultados
    save_results(df, velocities, cumulative_times, output_filepath)

if __name__ == "__main__":
    main()