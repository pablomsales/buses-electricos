import os
from time import time

from config import Config
from core.model import Model


def main():
    start_time = time()

    name = "linea_d2_algoritmo_simulation"

    data = os.path.join("data", f"{name}.csv")

    config = Config(electric=True, euro_standard="EURO_6")

    model = Model(
        name=name,
        filepath=data,
        bus=config.create_bus(),
        emissions=config.create_emissions(),
        mode="simulation",
    )

    model.consumption_and_emissions()

    print(f"Tiempo ejecucion: {time() - start_time}")


if __name__ == "__main__":
    main()
