"""
Proyecto: Optimización de Rutas y Análisis de Sostenibilidad en Autobuses Eléctricos Urbanos

Autores:

- Chakhoyan Grigoryan, Razmik
  Correo: chakhoyanrazmik@gmail.com
  LinkedIn: https://www.linkedin.com/in/chakhoyanrazmik

- Menéndez Sales, Pablo
  Correo: pablomenendezsales@gmail.com
  LinkedIn: https://www.linkedin.com/in/pablo-m-sales

Fecha de creación: 12/07/2024
Última modificación: 09/09/2024
"""


################################################
#################   OBSOLETO   #################
################################################


import pandas as pd
import os
from geopy.distance import great_circle
import overpy

def get_closest_speed_limit(coordinates, radius):
    lat, lon = coordinates
    api = overpy.Overpass()

    # Query based on a flexible radius
    for r in [radius, radius * 2, radius * 4]:  # Try increasing radius if no results found
        result = api.query(f"""
            way(around:{r},{lat},{lon}) ["maxspeed"];
            (._;>;);
            out body;
        """)

        closest_road = None
        min_distance = float('inf')
        
        for way in result.ways:
            for node in way.nodes:
                distance = great_circle(coordinates, (node.lat, node.lon)).meters
                if distance < min_distance:
                    min_distance = distance
                    closest_road = way

        if closest_road:
            speed_limit_str = closest_road.tags.get("maxspeed", "n/a")
            try:
                speed_limit = int(speed_limit_str)
                # Cap the speed limit at 50 km/h
                speed_limit = min(speed_limit, 50)
            except ValueError:
                road_type = closest_road.tags.get("highway", None)
                speed_limit = 30 if road_type in ["residential", "living_street"] else 50
            return speed_limit
    
    return 30  # Default if no road is found

def process_csv(file_path, radius):
    # Read the CSV file
    df = pd.read_csv(file_path)

    results = []
    
    # Iterate over each row in the DataFrame
    for _, row in df.iterrows():
        lat = row['Latitud']
        lon = row['Longitud']
        alt = row['Altitud(m)']
        coordinates = (lat, lon)
        speed_limit = get_closest_speed_limit(coordinates, radius)
        results.append({
            'Latitud': lat,
            'Longitud': lon,
            'Altitud': alt,
            'Limite': speed_limit
        })

    return results

# Main logic
csv_file_path = os.path.join("data", "linea_d2_algoritmo.csv")
radius = 100  # Example radius
results = process_csv(csv_file_path, radius)

# Optionally, save the results to a new CSV file
results_df = pd.DataFrame(results)
results_df.to_csv(os.path.join("src", "simulation", "speed_limits", "limits", "limits_linea_d2_algoritmo.csv"), index=False)

print("Processing completed.")
