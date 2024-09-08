import os

from core.model import Model
from core.model_config import ModelConfig


def main():
    """
    Función principal para ejecutar la simulación del modelo.

    - Configura los parámetros del modelo en función de si es eléctrico o no.
    - Crea una instancia del modelo con la configuración proporcionada.
    - Ejecuta el modelo durante el número de días especificado.
    """
    name = "linea_d2_simulation"

    data = os.path.join("data", "linea_d2", "linea_d2_simulation.csv")

    ELECTRIC = True

    days = 1

    if ELECTRIC:
        model_config = ModelConfig(
            electric=ELECTRIC,
            name=name,
            filepath=data,
            simulation=True,
            charging_point_id=1,
            min_battery_charge=20,
            max_battery_charge=80,
            initial_capacity_kWh=98 * 4,  # se opta por expresarlo como múltiplos de 98
            engine_max_power=230,  # kW
            bus_mass=15000,  # masa sin contar la batería
        )

    else:
        model_config = ModelConfig(
            electric=ELECTRIC,
            name=name,
            filepath=data,
            simulation=True,
            engine_max_power=230,  # kW
            bus_mass=18000,  # masa total del bus, para hacer comparaciones justas con el bus eléctrico, poner una masa ligeramente mayor (1500-3000 kg)
        )

    model = Model(config=model_config)

    model.run(n_days=days)


if __name__ == "__main__":
    main()
