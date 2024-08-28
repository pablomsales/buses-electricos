import os
from time import time

from config import Config
from core.model import Model


def main():
    start_time = time()

    name = "linea_d2_simulation_electric"

    data = os.path.join("data", "linea_d2_simulation.csv")

    config = Config(electric=False)

    model = Model(
        name=name,
        filepath=data,
        bus=config.create_bus(),
        emissions=config.create_emissions(),
        mode="simulation",
    )

    model.consumption_and_emissions()
    model.plot_combined_profiles()
    model.plot_map()

    print(f"Tiempo ejecucion: {time() - start_time}")


if __name__ == "__main__":
    main()
