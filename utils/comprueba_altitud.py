import srtm
import pandas as pd

def get_elevation(lat, lon):
    srtm_data = srtm.get_data()
    elevation = srtm_data.get_elevation(lat, lon)
    return elevation

def calculate_precision(csv_file):
    # Leer el archivo CSV
    df = pd.read_csv(csv_file)
    
    # Verificar que las columnas necesarias están presentes
    if not all(col in df.columns for col in ['Latitud', 'Longitud', 'Altitud(m)']):
        raise ValueError("El archivo CSV debe contener las columnas 'Latitud', 'Longitud', 'Altitud(m)'")
    
    # Listas para almacenar las diferencias y altitudes reales
    differences = []
    real_altitudes = []
    
    # Iterar a través de las filas del DataFrame
    for index, row in df.iterrows():
        lat = row['Latitud']
        lon = row['Longitud']
        altitud_medida = row['Altitud(m)']
        
        # Obtener la altitud real usando get_elevation
        altitud_real = get_elevation(lat, lon)
        
        # Verificar que la altitud real no sea cero para evitar división por cero
        if altitud_real == 0:
            raise ValueError(f"Altitud real es cero en la fila {index}. No se puede calcular el error porcentual.")
        
        # Calcular la diferencia absoluta
        diferencia = abs(altitud_medida - altitud_real)
        differences.append(diferencia)
        real_altitudes.append(altitud_real)
    
    # Calcular la diferencia media absoluta
    diferencia_media_absoluta = sum(differences) / len(differences)
    
    # Calcular la altitud real promedio
    altitud_real_promedio = sum(real_altitudes) / len(real_altitudes)
    
    # Calcular el índice de precisión (0 a 1)
    precision = 1 - (diferencia_media_absoluta / altitud_real_promedio)
    
    # Asegurarse de que la precisión no sea menor que 0
    precision = max(0, precision)
    
    return precision

# Ejemplo de uso
csv_file = 'data\prueba_tren.csv'
precision = calculate_precision(csv_file)
print(f'Índice de precisión: {precision:.2f}')
