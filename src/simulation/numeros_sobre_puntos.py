import os
import pandas as pd
import folium

# Leer los archivos CSV
df_limits = pd.read_csv(os.path.join('src', 'simulation', 'speed_limits', 'limits', 'limits_linea_d2_algoritmo.csv'))
df_stops = pd.read_csv(os.path.join('src', 'simulation', 'speed_profile', 'stops', 'stops.csv'))

# Calcular el promedio de las coordenadas para centrar el mapa
avg_lat = (df_limits['Latitud'].mean() + df_stops['Latitud'].mean()) / 2
avg_lng = (df_limits['Longitud'].mean() + df_stops['Longitud'].mean()) / 2

# Crear el mapa centrado
m = folium.Map(location=[avg_lat, avg_lng], zoom_start=14)

# Añadir las coordenadas y los números del primer DataFrame (df_limits) al mapa
for i, row in df_limits.iterrows():
    folium.Marker(
        location=[row['Latitud'], row['Longitud']],
        icon=folium.DivIcon(html=f'<div style="font-size: 12px; color: black;">{i + 2}</div>')
    ).add_to(m)

# Añadir las coordenadas y los números del segundo DataFrame (df_stops) al mapa
for i, row in df_stops.iterrows():
    folium.Marker(
        location=[row['Latitud'], row['Longitud']],
        icon=folium.DivIcon(html=f'<div style="font-size: 12px; color: red;">{i + 2}</div>')
    ).add_to(m)

# Guardar el mapa en un archivo HTML
output_path = os.path.join('src', 'simulation', 'numeros_sobre_puntos.html')
m.save(output_path)
