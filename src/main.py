import os
from time import time

from config import bus_instance, emissions_instance
from core.model import Model


def main():
    start_time = time()

    data = os.path.join("data", "linea_d2_algoritmo_simulation.csv")

    model = Model(
        name="linea_d2_algoritmo_simulation",
        filepath=data,
        bus=bus_instance,
        emissions=emissions_instance,
        mode="simulation",
    )

    model.consumption_and_emissions()
    model.plot_combined_profiles()
    model.plot_map()
    for sect in model.route.sections:
        print(sect)
        # print("-------------------")
        # print(sect._calculate_effective_forces())

    print(f"Tiempo ejecucion: {time() - start_time}")


if __name__ == "__main__":
    main()
