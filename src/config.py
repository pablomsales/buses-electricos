from core.bus.bus import Bus
from core.bus.engine import Engine
from core.bus.fuel import Fuel
from core.emissions import Emissions

# Crear una instancia de Fuel
fuel_instance = Fuel(fuel_type="diesel")

# Crear una instancia de Engine con el fuel
engine_instance = Engine(
    engine_type="combustion",  # Puede ser 'combustion' o 'electric'
    fuel=fuel_instance,
    max_power=300,  # kW
    efficiency=0.35,  # 0 a 1
)

# Crear una instancia de Bus con el motor
bus_instance = Bus(
    mass=18000,
    drag_coefficient=0.8,
    frontal_area=13.0,
    rolling_resistance_coefficient=0.01,
    engine=engine_instance,
)

# Crear una instancia de Emissions con el estándar EURO deseado
emissions_instance = Emissions(euro_standard="EURO_6")
