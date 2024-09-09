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

from config import DATA, DAYS, ELECTRIC, NAME
from core.model import Model
from core.model_config import ModelConfig


def main():
    """
    Función principal para ejecutar la simulación del modelo.

    - Configura los parámetros del modelo en función de si es eléctrico o no.
    - Crea una instancia del modelo con la configuración proporcionada.
    - Ejecuta el modelo durante el número de días especificado.
    """

    if ELECTRIC:
        model_config = ModelConfig(
            electric=ELECTRIC,
            name=NAME,
            filepath=DATA,
            charging_point_id=1,
            min_battery_charge=20,
            max_battery_charge=80,
            initial_capacity_kWh=392,
        )

    else:
        model_config = ModelConfig(
            electric=ELECTRIC,
            name=NAME,
            filepath=DATA,
        )

    model = Model(config=model_config)

    model.run(n_days=DAYS)


if __name__ == "__main__":
    main()
