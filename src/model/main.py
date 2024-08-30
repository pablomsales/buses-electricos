import os
from time import time

from config import Config
from core.model import Model


def main():
    start_time = time()

    name = "linea_d2_simulation_electric"

    data = os.path.join("data", "linea_d2", "linea_d2_simulation.csv")

    config = Config(electric=True)

    model = Model(
        name=name,
        filepath=data,
        bus=config.create_bus(),
        emissions=config.create_emissions(),
        mode="simulation",
    )

    print(f"Tiempo ejecucion: {time() - start_time}")


if __name__ == "__main__":
    main()
