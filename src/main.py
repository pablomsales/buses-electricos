import os
from time import time

from config import bus_instance, emissions_instance, engine_instance, fuel_instance
from core.model import Model


def main():
    start_time = time()

    data = os.path.join("data", "sandbox", "linea_d2_1_16.csv")

    try:
        real_model = Model(
            filepath=data,
            bus=bus_instance,
            emissions=emissions_instance,
            mode="real",
        )

        real_model.consumption_and_emissions

    except ValueError as e:
        print(f"Error: {e}")

    print(f"Tiempo ejecucion: {time() - start_time}")


if __name__ == "__main__":
    main()
