from model.model_config import ModelConfig
from src.model.core.model import Model


class Fitness:

    def __init__(self):
        self.model_config = ModelConfig(electric=True)

    def evaluate(self, parameters: dict):

        # desempaquetar diccionario de parameters

        # Establecer parametros en ModelConfig
        bus = self.model_config.create_bus(
            initial_capacity_kWh,
            engine_max_power,
            bus_mass,  # antes que nada hay que sumar bus_mass y battery_mass !!!
            time_between_charges,
        )
        emissions = self.model_config.create_bus()

        # Inicializar Model() con ModelConfig()
        model_name = ...
        data = ...
        model = Model(
            name=model_name,
            filepath=data,
            bus=bus,
            emissions=emissions,
            mode="simulation",
        )
