import os
import pandas as pd

# Cargar el archivo Excel
df = pd.read_csv(os.join.path('data', 'sandbox', 'linea_d2_1_8.csv'))

# Eliminar las filas pares
df = df.iloc[1::2]

# Guardar el archivo Excel modificado
df.to_csv(os.join.path('data', 'sandbox', 'linea_d2_1_16.csv'))
