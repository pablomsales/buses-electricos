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

import os
import sys

# Fijamos la ruta base para manejar correctamente el resto de rutas del proyecto
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
sys.path.append(PROJECT_ROOT)

# Nombre del proyecto o simulación, usado para identificar las simulaciones ejecutadas.
NAME = "linea_d2_simulation"

# Ruta al archivo CSV con los datos de la simulación.
DATA = os.path.join(PROJECT_ROOT, "data", "line_data", "line_data_simulation.csv")

# Bool para indicar si el modelo de autobus es electrico o de combustion
ELECTRIC = True

# Numero de dias de simulacion
DAYS = 1
