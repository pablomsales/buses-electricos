import os
from time import time

from models.real_model import RealModel
from src.core.bus.bus import Bus
from src.core.bus.engine import Engine
from src.core.bus.fuel import Fuel
from src.core.emissions import Emissions


def main():
    start_time = time()
    data = os.path.join("data", "linea_d2_1_16.csv")

    # Crear una instancia de Fuel
    fuel_instance = Fuel(fuel_type="diesel")

    # Crear una instancia de Engine con el fuel
    engine_instance = Engine(
        engine_type="combustion",  # Puede ser 'combustion' o 'electric'
        fuel=fuel_instance,
        max_power=200,  # kW
        efficiency=0.35,  # 0 a 1
    )

    # Crear una instancia de Bus con el motor
    bus_instance = Bus(
        mass=12000,
        drag_coefficient=0.65,
        frontal_area=8.0,
        rolling_resistance_coefficient=0.01,
        engine=engine_instance,
    )

    # Crear una instancia de Emissions con el estándar EURO deseado
    euro_standard = "EURO_6"
    emissions_instance = Emissions(euro_standard)

    try:
        real_model = RealModel(
            filepath=data, bus=bus_instance, emissions=emissions_instance
        )

        for section in real_model.route.sections:
            print(section)

        # real_model.route.plot_map(output_file="linea_D2.html")
        print(f"Tiempo ejecucion: {time() - start_time}")

        real_model.route.combined_profiles_plot()

    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
