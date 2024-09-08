import numpy as np
from core.bus.engine.base_engine import BaseEngine
from utils.constants import TRAVELLER_WEIGHT

class Bus:
    """
    Clase para representar un autobús.
    """

    def __init__(
        self,
        bus_mass,
        drag_coefficient,
        frontal_area,
        rolling_resistance_coefficient,
        engine,
    ):
        """
        Inicializa una instancia de la clase Bus.

        Args:
            bus_mass (float): Masa del autobús en kg.
            drag_coefficient (float): Coeficiente de arrastre del autobús.
            frontal_area (float): Área frontal del autobús en m².
            rolling_resistance_coefficient (float): Coeficiente de resistencia al rodamiento del autobús.
            engine (BaseEngine): Objeto que representa el motor del autobús.

        Raises:
            ValueError: Si el motor proporcionado no es una instancia de BaseEngine o sus subclases.
        """
        self.num_travellers = self.update_num_travellers()
        self._drag_coefficient = drag_coefficient
        self._frontal_area = frontal_area
        self._rolling_resistance_coefficient = rolling_resistance_coefficient
        self.engine = engine
        if self.engine.electric:
            self._bus_mass = bus_mass + self.engine.battery.initial_capacity_kWh * 6 # 6 kg por kWh
        else:
            self._bus_mass = bus_mass

    @property
    def total_mass(self):
        """
        Obtiene la masa total del autobús en kg, incluyendo pasajeros.

        Returns:
            float: Masa total del autobús en kg.
        """
        return self.bus_mass + (self.num_travellers * TRAVELLER_WEIGHT)

    @property
    def bus_mass(self):
        """
        Obtiene la masa del autobús sin pasajeros en kg.

        Returns:
            float: Masa del autobús en kg.
        """
        return self._bus_mass

    @bus_mass.setter
    def bus_mass(self, value):
        """
        Establece la masa del autobús en kg.

        Args:
            value (float): La nueva masa del autobús en kg.

        Notes:
            La masa del autobús debe ser un valor positivo.
        """
        if value > 0:
            self._bus_mass = value

    @property
    def drag_coefficient(self):
        """
        Obtiene el coeficiente de arrastre del autobús.

        Returns:
            float: Coeficiente de arrastre del autobús.
        """
        return self._drag_coefficient

    @drag_coefficient.setter
    def drag_coefficient(self, value):
        """
        Establece el coeficiente de arrastre del autobús.

        Args:
            value (float): Nuevo valor del coeficiente de arrastre.

        Notes:
            El coeficiente de arrastre debe estar en el rango (0, 1).
        """
        if 0 < value < 1:  # valores típicos para el coeficiente de arrastre
            self._drag_coefficient = value

    @property
    def frontal_area(self):
        """
        Obtiene el área frontal del autobús en m².

        Returns:
            float: Área frontal del autobús en m².
        """
        return self._frontal_area

    @frontal_area.setter
    def frontal_area(self, value):
        """
        Establece el área frontal del autobús en m².

        Args:
            value (float): Nueva área frontal del autobús en m².

        Notes:
            El área frontal debe ser un valor positivo.
        """
        if value > 0:
            self._frontal_area = value

    @property
    def rolling_resistance_coefficient(self):
        """
        Obtiene el coeficiente de resistencia al rodamiento del autobús.

        Returns:
            float: Coeficiente de resistencia al rodamiento.
        """
        return self._rolling_resistance_coefficient

    @rolling_resistance_coefficient.setter
    def rolling_resistance_coefficient(self, value):
        """
        Establece el coeficiente de resistencia al rodamiento del autobús.

        Args:
            value (float): Nuevo coeficiente de resistencia al rodamiento.

        Notes:
            El coeficiente de resistencia al rodamiento debe ser un valor positivo.
        """
        if value > 0:
            self._rolling_resistance_coefficient = value

    @property
    def engine(self):
        """
        Obtiene el objeto del motor que representa el motor del autobús.

        Returns:
            BaseEngine: El motor del autobús.
        """
        return self._engine

    @engine.setter
    def engine(self, value):
        """
        Establece el motor del autobús.

        Args:
            value (BaseEngine): El nuevo motor para el autobús.

        Raises:
            ValueError: Si el valor no es una instancia de BaseEngine o sus subclases.
        """
        if isinstance(value, BaseEngine):
            self._engine = value
        else:
            print(type(value))
            raise ValueError(
                "Engine must be an instance of BaseEngine or its subclasses"
            )

    @staticmethod
    def update_num_travellers():
        """
        Actualiza el número de pasajeros en el autobús utilizando una distribución normal.

        Returns:
            int: Número de pasajeros, con un valor ajustado y redondeado a los límites establecidos.
        """
        # Fija la semilla para la reproducibilidad
        np.random.seed(16)
        # Genera el número de pasajeros
        num_travellers = np.random.normal(loc=40, scale=30)
        # Recorta a los límites establecidos y redondea a entero
        return round(np.clip(num_travellers, 0, 146))

    def get_battery_state_of_charge(self):
        """
        Obtiene el estado de carga de la batería del motor del autobús.

        Returns:
            float: Estado de carga de la batería como porcentaje.
        """
        return self.engine.get_battery_state_of_charge()

    def get_battery_degradation_in_section(self):
        """
        Obtiene la degradación de la batería en la sección actual.

        Returns:
            float: Degradación de la batería en la sección.
        """
        return self.engine.get_battery_degradation_in_section()

    def get_battery_state_of_health(self):
        """
        Obtiene el estado de salud de la batería del motor del autobús.

        Returns:
            float: Estado de salud de la batería como porcentaje.
        """
        return self.engine.get_battery_state_of_health()

    def get_battery_capacity_kWh(self):
        """
        Obtiene la capacidad de la batería del motor del autobús en kWh.

        Returns:
            float: Capacidad de la batería en kilovatios hora.
        """
        return self.engine.get_battery_capacity_kWh()

    def get_total_time_below_min_soc(self):
        """
        Obtiene el tiempo total en el que el estado de carga de la batería estuvo por debajo del mínimo.

        Returns:
            float: Tiempo total en segundos con la batería por debajo del estado de carga mínimo.
        """
        return self.engine.get_total_time_below_min_soc()

    def __str__(self):
        """
        Devuelve una representación en cadena de las características del autobús,
        incluyendo masa, coeficiente de arrastre, área frontal, coeficiente de resistencia
        al rodamiento y características del motor.

        Returns:
            str: Una cadena con la información detallada del autobús.
        """
        return (
            f"Bus Characteristics:\n"
            f"Mass: {self.mass} kg\n"
            f"Drag Coefficient: {self.drag_coefficient}\n"
            f"Frontal Area: {self.frontal_area} m²\n"
            f"Rolling Resistance Coefficient: {self.rolling_resistance_coefficient}\n"
            f"{str(self.engine)}"
        )
