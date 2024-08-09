import os
import pandas as pd
import folium

# Leer el archivo CSV
name = 'limits_linea_d2_algoritmo'
df = pd.read_csv(os.path.join('src', 'simulation', 'limits', f'{name}.csv'))

# Crear un mapa centrado en el promedio de las coordenadas
m = folium.Map(location=[df['Latitud'].mean(), df['Longitud'].mean()], zoom_start=14)

# Función para seleccionar la imagen correspondiente al valor
def get_icon_image(limit):
    if limit == 30:
        return os.path.join('src', 'simulation', 'icons', 'speed_30.png')
    elif limit == 50:
        return os.path.join('src', 'simulation', 'icons', 'speed_50.png')

# Añadir las coordenadas y las imágenes al mapa
for _, row in df.iterrows():
    icon_image = get_icon_image(row['Limite'])
    
    icon = folium.CustomIcon(
        icon_image,
        icon_size=(25, 25),  # Tamaño de la imagen
    )
    
    folium.Marker(
        location=[row['Latitud'], row['Longitud']],
        icon=icon
    ).add_to(m)

# Guardar el mapa en un archivo HTML
m.save(os.path.join('src', 'simulation', 'maps', f'{name}.html'))
