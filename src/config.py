from core.bus.bus import Bus
from core.bus.engine.battery import Battery
from core.bus.engine.electrical_engine import ElectricalEngine
from core.bus.engine.fuel_engine import FuelEngine
from core.bus.fuel import Fuel
from core.emissions import Emissions

# Crear una instancia de Fuel
# fuel_instance = Fuel(fuel_type="diesel")

# Crear una instancia de Engine con el fuel
# engine_instance = FuelEngine(
#     fuel=fuel_instance,
#     max_power=200,  # kW
#     efficiency=0.35,  # 0 a 1
# )

# Crear instancia de Battery
battery_instance = Battery(
    initial_capacity_ah=300,
    voltage_v=600,
    max_cycles=3000,
    initial_soc_percent=100,
    min_depth_of_discharge=80,
)

engine_instance = ElectricalEngine(
    max_power=240,
    efficiency=92,
    battery=battery_instance,
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
emissions_instance = Emissions(euro_standard="EURO_6")
