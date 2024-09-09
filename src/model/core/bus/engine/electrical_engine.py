"""
Proyecto: Optimización de Rutas y Análisis de Sostenibilidad en Autobuses Eléctricos Urbanos

Autores:

- Chakhoyan Grigoryan, Razmik
  Correo: chakhoyanrazmik@gmail.com
  LinkedIn: https://www.linkedin.com/in/chakhoyanrazmik

- Menéndez Sales, Pablo
  Correo: pablomenendezsales@gmail.com
  LinkedIn: https://www.linkedin.com/in/pablo-m-sales

Fecha de creación: 12/07/2024
Última modificación: 09/09/2024
"""


from core.bus.engine.base_engine import BaseEngine

class ElectricalEngine(BaseEngine):
    """
    La clase ElectricalEngine representa un motor eléctrico.
    """

    def __init__(self, max_power, efficiency, battery):
        """
        Inicializa una instancia de la clase ElectricalEngine.

        Args:
            max_power (float): La potencia máxima del motor en kilovatios (kW).
            efficiency (float): La eficiencia del motor en un rango de [0, 1].
            battery (Battery): La batería asociada con el motor eléctrico.
        """
        super().__init__(max_power, efficiency)
        self.battery = battery
        self.electric = True

    @property
    def battery_state_of_health(self):
        """
        Obtiene el estado de salud de la batería.

        Returns:
            float: El estado de salud de la batería como un porcentaje.
        """
        return self.battery.state_of_health

    def consumption(self, power, time, km=None):
        """
        Calcula el consumo eléctrico en Wh.

        Args:
            power (float): La potencia solicitada en Watts.
            time (float): El tiempo durante el cual se utiliza la potencia en segundos.
            km (float, opcional): Kilómetros recorridos, por defecto es None.

        Returns:
            dict: Un diccionario con el consumo en Wh (vatios hora), Ah (amperios hora),
                  L/h (litros por hora, 0 para motores eléctricos), y L/km (litros por kilómetro, 0 para motores eléctricos).
        """
        power = self._adjust_power(power)
        hours = time / 3600  # convierte segundos a horas

        # Calcula el consumo en Wh y Ah
        watts_hour = power * hours
        ampers_hour = watts_hour / self.battery.voltage_v

        self.battery.update_soc_and_degradation(ampers_hour, time)

        return {
            "Wh": watts_hour,
            "Ah": ampers_hour,
            "L/h": 0,  # 0 para ElectricalEngine
            "L/km": 0,  # "" "" ""
        }

    def get_battery_state_of_charge(self):
        """
        Obtiene el estado de carga de la batería.

        Returns:
            float: El estado de carga de la batería como un porcentaje.
        """
        return self.battery.state_of_charge_percent

    def get_battery_degradation_in_section(self):
        """
        Obtiene la degradación de la batería en la sección actual.

        Returns:
            float: La degradación de la batería en la sección.
        """
        return self.battery.degradation_in_section

    def get_battery_state_of_health(self):
        """
        Obtiene el estado de salud de la batería.

        Returns:
            float: El estado de salud de la batería como un porcentaje.
        """
        return self.battery.state_of_health

    def get_battery_capacity_kWh(self):
        """
        Obtiene la capacidad inicial de la batería en kWh.

        Returns:
            float: La capacidad inicial de la batería en kilovatios hora.
        """
        return self.battery.initial_capacity_kWh

    def get_total_time_below_min_soc(self):
        """
        Obtiene el tiempo total en el que el estado de carga de la batería estuvo por debajo del mínimo.

        Returns:
            float: El tiempo total en segundos en que la batería estuvo por debajo del estado de carga mínimo.
        """
        return self.battery.total_time_below_min_soc

    def __str__(self):
        """
        Devuelve una representación en cadena del motor eléctrico, incluyendo su tipo,
        potencia máxima y eficiencia.

        Returns:
            str: Una cadena con la información del motor eléctrico.
        """
        return "Engine Type: Electric\n" + super().__str__()
