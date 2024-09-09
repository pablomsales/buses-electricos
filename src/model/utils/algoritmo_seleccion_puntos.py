################################################
#################   OBSOLETO   #################
################################################


import os

import pandas as pd
from config import PROJECT_ROOT
from geopy.distance import geodesic

# Cargar el CSV en un DataFrame
df = pd.read_csv(os.path.join(PROJECT_ROOT, "data", "linea_d2.csv"))


# Función para calcular la distancia entre dos puntos geográficos
def calcular_distancia(lat1, lon1, lat2, lon2):
    return geodesic((lat1, lon1), (lat2, lon2)).meters


# Inicializar la lista de puntos seleccionados con el primer punto
puntos_seleccionados = [df.iloc[0]]
ultima_lat = df.iloc[0]["Latitud"]
ultima_lon = df.iloc[0]["Longitud"]

# Iterar sobre el DataFrame para seleccionar puntos a una distancia de al menos 100 metros
for index, row in df.iterrows():
    lat = row["Latitud"]
    lon = row["Longitud"]
    distancia = calcular_distancia(ultima_lat, ultima_lon, lat, lon)
    if distancia >= 25:  # Distancia deseada en metros
        puntos_seleccionados.append(row)
        ultima_lat = lat
        ultima_lon = lon

# Crear un nuevo DataFrame con los puntos seleccionados
df_filtrado = pd.DataFrame(puntos_seleccionados)

# Guardar el nuevo DataFrame en un nuevo archivo CSV
df_filtrado.to_csv(os.path.join("data", "linea_d2_algoritmo.csv"), index=False)
