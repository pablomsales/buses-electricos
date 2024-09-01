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
        mode="simulation",
        charging_point_id=1,
        initial_capacity_kWh=294,
        engine_max_power=230000,
        bus_mass=20000,
    )
    model = Model(config=model_config)

    model.run(n_iters=1)

    print(f"Tiempo ejecucion: {time() - start_time}")


if __name__ == "__main__":
    main()
