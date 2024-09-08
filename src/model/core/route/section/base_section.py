import math
from geopy.distance import geodesic
from core.route.resistance_calculator import ResistanceCalculator

class BaseSection:
    """
    Clase para representar una sección de una ruta.
    """

    def __init__(self, coordinates, bus, emissions):
        """
        Inicializa una instancia de BaseSection con coordenadas, un bus, y emisiones.

        Args:
            coordinates (tuple): Una tupla que contiene 2 tuplas: coordenadas de inicio y fin.
            bus: Instancia de la clase Bus.
            emissions: Instancia de la clase Emissions.
        """
        self._start = coordinates[0]  # Coordenadas del inicio de la sección
        self._end = coordinates[1]    # Coordenadas del final de la sección

        self.bus = bus
        self.emissions = emissions

        self._average_speed = self._calculate_average_speed()
        self._acceleration = self._calculate_acceleration()
        self._grade_angle = self.grade_angle

        self.resistance_calculator = ResistanceCalculator(
            self.bus,
            self._average_speed,
            self._acceleration,
            self._grade_angle,
        )

    @property
    def start(self) -> tuple[float, float, float]:
        """
        Obtiene las coordenadas de inicio de la sección.

        Returns:
            tuple: Coordenadas de inicio (latitud, longitud, altitud).
        """
        return self._start

    @property
    def end(self) -> tuple[float, float, float]:
        """
        Obtiene las coordenadas de fin de la sección.

        Returns:
            tuple: Coordenadas de fin (latitud, longitud, altitud).
        """
        return self._end

    @property
    def length(self) -> float:
        """
        Calcula la longitud de la sección en metros utilizando la distancia geodésica.

        Returns:
            float: Longitud de la sección en metros.
        """
        lat_0, long_0 = self.start[0], self.start[1]  # Latitud y longitud de inicio
        lat_1, long_1 = self.end[0], self.end[1]      # Latitud y longitud de fin
        return geodesic((lat_0, long_0), (lat_1, long_1)).meters

    @property
    def grade_angle(self) -> float:
        """
        Calcula el ángulo de inclinación de la sección en grados.

        Returns:
            float: Ángulo de inclinación en grados.
        """
        delta_altitude = self.end[2] - self.start[2]
        return math.degrees(math.atan(delta_altitude / self.length)) if self.length != 0 else 0

    def _calculate_average_speed(self) -> float:
        """
        Calcula la velocidad promedio de la sección.

        Returns:
            float: Velocidad promedio en m/s.
        """
        return (self.start_speed + self.end_speed) / 2

    def _calculate_acceleration(self) -> float:
        """
        Calcula la aceleración constante de la sección.

        Returns:
            float: Aceleración en m/s².
        """
        delta_v = self.end_speed - self.start_speed
        delta_t = self.duration_time
        return delta_v / delta_t if delta_t != 0 else 0

    @property
    def air_resistance(self) -> float:
        """
        Obtiene la resistencia del aire calculada por el ResistanceCalculator.

        Returns:
            float: Resistencia del aire en Newtons.
        """
        return self.resistance_calculator.air_resistance

    @property
    def inertia(self) -> float:
        """
        Obtiene la inercia calculada por el ResistanceCalculator.

        Returns:
            float: Inercia en Newtons.
        """
        return self.resistance_calculator.inertia

    @property
    def grade_resistance(self) -> float:
        """
        Obtiene la resistencia por pendiente calculada por el ResistanceCalculator.

        Returns:
            float: Resistencia por pendiente en Newtons.
        """
        return self.resistance_calculator.grade_resistance

    @property
    def rolling_resistance(self) -> float:
        """
        Obtiene la resistencia por rodadura calculada por el ResistanceCalculator.

        Returns:
            float: Resistencia por rodadura en Newtons.
        """
        return self.resistance_calculator.rolling_resistance

    @property
    def total_resistance(self) -> float:
        """
        Obtiene la resistencia total calculada por el ResistanceCalculator.

        Returns:
            float: Resistencia total en Newtons.
        """
        return self.resistance_calculator.total_resistance

    @property
    def work(self) -> float:
        """
        Calcula el trabajo (en Julios) realizado en la sección.

        Returns:
            float: Trabajo en Julios.
        """
        force = self.total_resistance  # Fuerza en Newtons
        distance = self.length         # Distancia en metros
        return force * distance * math.cos(math.radians(self.grade_angle))

    @property
    def instant_power(self) -> float:
        """
        Calcula la potencia instantánea en la sección en Watts.

        Returns:
            float: Potencia instantánea en Watts.
        """
        return self.work / self.duration_time  # Potencia en Watts

    @property
    def consumption(self) -> dict[str, float]:
        """
        Calcula el consumo de la sección.

        Returns:
            dict: Un diccionario con los valores de consumo.
        """
        return self.bus.engine.consumption(
            power=self.instant_power,
            time=self.duration_time,
            km=self.length / 1000,
        )

    @property
    def section_emissions(self) -> dict[str, float]:
        """
        Calcula las emisiones de la sección.

        Returns:
            dict: Un diccionario con los valores de emisiones en gramos por segundo.
        """
        power_kw = self.instant_power / 1000  # Convertir Watts a kW
        fuel_consumption_rate = self.consumption["L/h"] / 3600  # Convertir L/h a L/s
        return self.emissions.calculate_emissions(
            power_kw,
            fuel_consumption_rate=fuel_consumption_rate,
        )

    @property
    def duration_time(self):
        """
        Obtiene la duración de la sección en segundos.

        Returns:
            float: Duración de la sección en segundos.
        """
        return self._end_time - self._start_time

    def get_battery_degradation_in_section(self):
        """
        Obtiene la degradación de la batería en la sección.

        Returns:
            float: Degradación de la batería.
        """
        return self.bus.get_battery_degradation_in_section()

    def get_battery_state_of_charge(self):
        """
        Obtiene el estado de carga de la batería.

        Returns:
            float: Estado de carga de la batería.
        """
        return self.bus.get_battery_state_of_charge()

    def get_battery_state_of_health(self):
        """
        Obtiene el estado de salud de la batería.

        Returns:
            float: Estado de salud de la batería.
        """
        return self.bus.get_battery_state_of_health()

    def __str__(self):
        """
        Representación en cadena de la sección, incluyendo sus características
        y métricas calculadas, como resistencias, trabajo, potencia, consumo y emisiones.

        Returns:
            str: Cadena de texto con la información de la sección.
        """
        emissions_str = "\n".join(
            [f"{k}: {v:.6f} g/s" for k, v in self.section_emissions.items()]
        )

        if self.bus.engine.electric:
            return (
                f"\n---------------------------------------------------"
                f"\nSection from {self.start[0]} º, {self.start[1]} º, {round(self.start[2], 2)} m "
                f"to\n{' ' * (len('Section from ')-1)} {self.end[0]} º, {self.end[1]} º, {round(self.end[2], 2)} m"
                f"\n---------------------------------------------------"
                f"\nSpeeds: {round(self.start_speed, 2)} m/s to {round(self.end_speed, 2)} m/s, "
                f"\nAir Resistance: {self.air_resistance:.2f} N, "
                f"\nInertia: {self.inertia:.2f} N, "
                f"\nGrade Resistance: {self.grade_resistance:.2f} N, "
                f"\nRolling Resistance: {self.rolling_resistance:.2f} N, "
                f"\nTotal Resistance: {self.total_resistance:.2f} N\n"
                f"\nWork: {self.work:.2f} J"
                f"\nRequired Power: {self.instant_power:.2f} W"
                f"\nConsumption: {self.consumption}"
                f"\n\nEmissions:\n{emissions_str}"
                f"\n\nBattery SoC: {self.get_battery_state_of_charge()}"
                f"\nBattery degradation: {self.get_battery_degradation_in_section()}"
                f"\nBattery DoD (Health): {self.get_battery_state_of_health()}"
                f"\n"
            )
        else:
            return (
                f"\n---------------------------------------------------"
                f"\nSection from {self.start[0]} º, {self.start[1]} º, {round(self.start[2], 2)} m "
                f"to\n{' ' * (len('Section from ')-1)} {self.end[0]} º, {self.end[1]} º, {round(self.end[2], 2)} m"
                f"\n---------------------------------------------------"
                f"\nSpeeds: {round(self.start_speed, 2)} m/s to {round(self.end_speed, 2)} m/s, "
                f"\nAir Resistance: {self.air_resistance:.2f} N, "
                f"\nInertia: {self.inertia:.2f} N, "
                f"\nGrade Resistance: {self.grade_resistance:.2f} N, "
                f"\nRolling Resistance: {self.rolling_resistance:.2f} N, "
                f"\nTotal Resistance: {self.total_resistance:.2f} N\n"
                f"\nWork: {self.work:.2f} J"
                f"\nRequired Power: {self.instant_power:.2f} W"
                f"\nConsumption: {self.consumption}"
                f"\n\nEmissions:\n{emissions_str}"
                f"\n"
            )