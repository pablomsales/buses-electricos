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
DATA = os.path.join(PROJECT_ROOT, "data", "linea_d2", "linea_d2_simulation.csv")

# Bool para indicar si el modelo de autobus es electrico o de combustion
ELECTRIC = True

# Numero de dias de simulacion
DAYS = 1
