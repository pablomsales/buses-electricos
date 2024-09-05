import os
from time import time

from core.model import Model
from core.model_config import ModelConfig


def main():
    start_time = time()

    name = "linea_d2_simulation_electric"

    data = os.path.join("data", "linea_d2", "linea_d2_simulation.csv")

    model_config = ModelConfig(
        electric=True,
        name=name,
        filepath=data,
        simulation=True,
        charging_point_id=1,
        min_battery_charge=35,
        max_battery_charge=70,
        initial_capacity_kWh=98 * 4,
        engine_max_power=230,  # kW
        bus_mass=20000,
    )
    model = Model(config=model_config)

    model.run()

    print(f"\nTiempo de ejecución: {round(time() - start_time, 2)}s")


if __name__ == "__main__":
    main()
