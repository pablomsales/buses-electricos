from core.bus.engine.base_engine import BaseEngine
from core.bus.fuel import Fuel

class FuelEngine(BaseEngine):
    """
    Representa un motor de combustión.
    """

    def __init__(self, max_power, efficiency, fuel):
        """
        Inicializa un motor de combustión con la potencia máxima, eficiencia y combustible.

        Args:
            max_power (float): La potencia máxima del motor en Watts.
            efficiency (float): La eficiencia del motor en un rango de [0, 1].
            fuel (Fuel): El combustible utilizado por el motor.

        Raises:
            ValueError: Si el combustible no es una instancia de la clase Fuel.
        """
        super().__init__(max_power, efficiency)
        if not isinstance(fuel, Fuel):
            raise ValueError("fuel must be an instance of Fuel")
        self._fuel = fuel
        self.electric = False

    @property
    def fuel(self):
        """
        Obtiene el objeto Fuel que representa el combustible utilizado por el motor.

        Returns:
            Fuel: El combustible utilizado por el motor.
        """
        return self._fuel

    @fuel.setter
    def fuel(self, value):
        """
        Establece el combustible utilizado por el motor.

        Args:
            value (Fuel): El combustible nuevo para el motor.

        Raises:
            ValueError: Si el valor no es una instancia de la clase Fuel.
        """
        if isinstance(value, Fuel):
            self._fuel = value
        else:
            raise ValueError("fuel must be an instance of Fuel")

    def consumption(self, power, time, km) -> dict[str, float]:
        """
        Calcula el consumo de combustible.

        Args:
            power (float): La demanda de potencia en Watts.
            time (float): El periodo de tiempo en segundos durante el cual se aplica la potencia.
            km (float, opcional): La distancia recorrida en kilómetros (si está disponible).

        Returns:
            dict[str, float]: Un diccionario que contiene:
                - "Wh": Siempre 0 para un motor de combustión.
                - "L/h": Litros de combustible consumidos por hora.
                - "L/km": Litros de combustible consumidos por kilómetro (si se proporciona la distancia).

        Notes:
            Si la potencia es negativa, el consumo es cero.
            NOTA: Podría no ser 0 y ser una constante, dependiendo del comportamiento del motor.
        """
        # Si la potencia es negativa, el consumo es cero.
        if power < 0:
            return {
                "L/h": 0.0,
                "L/km": 0.0 if km is not None else None,
            }

        power = self._adjust_power(power)
        lhv = self.fuel.lhv  # Valor Calorífico Inferior del combustible

        # Calcula la energía utilizada
        energy = (power * time) / self._efficiency
        # Calcula el consumo de combustible en litros
        litres = energy / lhv

        consumption = {
            "L/h": litres / (time / 3600),  # Convierte el tiempo de segundos a horas
            "L/km": litres / km if km is not None else None,
        }

        return consumption
