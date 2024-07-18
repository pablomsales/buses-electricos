import os
from time import time

from bus import Bus
from route import Route


def main():
    start_time = time()
    data = os.path.join("data", "linea_d2.csv")
    bus_instance = Bus(
        mass=12000,
        drag_coefficient=0.65,
        frontal_area=8.0,
        rolling_resistance_coefficient=0.01,
    )

    try:
        route_instance = Route(filepath=data, bus=bus_instance)

        for section in route_instance.sections:
            print(section)

        route_instance.plot_map(output_file="linea_D2.html")
        print(f"Tiempo ejecucion: {time() - start_time}")

    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
