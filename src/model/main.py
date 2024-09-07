import os
from time import time

from core.model import Model
from core.model_config import ModelConfig


def main():
    start_time = time()

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
            initial_capacity_kWh=98 * 4,
            engine_max_power=230,  # kW
            bus_mass=20000,
        )
    
    else:
        model_config = ModelConfig(
            electric=ELECTRIC,
            name=name,
            filepath=data,
            simulation=True,
            engine_max_power=230,  # kW
            bus_mass=20000,
        )

    model = Model(config=model_config)

    model.run(n_iters=16*days)

    print(f"\nTiempo de ejecución: {round(time() - start_time, 2)}s")


if __name__ == "__main__":
    main()
