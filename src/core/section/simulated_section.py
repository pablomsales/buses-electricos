import math
from core.section.base_section import BaseSection

ACCELERATION_LIMIT = 0.6  # m/s^2
DECELERATION_LIMIT = -0.6  # m/s^2

class SimulatedSection(BaseSection):
    def __init__(self, coordinates, bus, emissions, speed_limit, start_speed=0.0, start_time=0.0):
        """
        Initialize a SimulatedSection with coordinates, bus, emissions, a single speed limit, 
        start speed, and start time.

        Args:
            coordinates (tuple): A tuple containing start and end coordinates.
            bus: Instance of the Bus class.
            emissions: Instance of the Emissions class.
            speed_limit (float): Speed limit (km/h) for the section.
            start_speed (float): Speed at the beginning of the section (m/s).
            start_time (float): Time at the beginning of the section (s).
        """
        self._speed_limit = speed_limit / 3.6  # Convertir km/h a m/s
        self._start_speed = start_speed
        self._end_speed = 0.0
        self._start_time = start_time
        self._end_time = 0.0
        self._start = coordinates[0]  # Coordenadas del inicio de la sección
        self._end = coordinates[1]    # Coordenadas del final de la sección
        
        # Llamar a la clase base para inicializar atributos necesarios
        super().__init__(coordinates, bus, emissions)

    def simulate(self):
        """
        Simulate the section by calculating the speed and time based on the speed limit and distance.
        """
        current_speed = self._start_speed

        # Calcular aceleración y velocidad final
        acceleration, final_speed = self.calculate_acceleration(current_speed, self._speed_limit, self.length)

        # Calcular el tiempo para recorrer la sección
        time_to_travel = self.calculate_time(acceleration, current_speed, final_speed)
        self._end_time = self._start_time + time_to_travel

        # Actualizar la velocidad al final de la sección
        self._end_speed = final_speed

    def calculate_acceleration(self, prev_speed, speed_limit, distance):
        """
        Calculate the acceleration needed to reach the speed limit or decelerate to stop.

        Args:
            prev_speed (float): Initial speed in m/s.
            speed_limit (float): Speed limit in m/s for the section.
            distance (float): Distance of the section in meters.

        Returns:
            float: Constant acceleration in m/s^2.
            float: Final speed reached in m/s.
        """
        total_resistance = self.total_resistance / self.bus.mass  # Resistance per unit mass (m/s^2)
        acceleration = (speed_limit**2 - prev_speed**2) / (2 * distance) - total_resistance

        if acceleration > ACCELERATION_LIMIT:
            acceleration = ACCELERATION_LIMIT
        elif acceleration < DECELERATION_LIMIT:
            acceleration = DECELERATION_LIMIT

        # Calcular la velocidad alcanzable al final de la sección
        achievable_speed = math.sqrt(max(prev_speed**2 + 2 * (acceleration + total_resistance) * distance, 0))
        return acceleration, achievable_speed

    def calculate_time(self, acceleration, prev_speed, final_speed):
        """
        Calculate the time needed to travel the section.

        Args:
            acceleration (float): Constant acceleration in m/s^2.
            prev_speed (float): Initial speed in m/s.
            final_speed (float): Final speed in m/s.

        Returns:
            float: Time needed in seconds.
        """
        if acceleration != 0:
            delta_t = (final_speed - prev_speed) / acceleration
        else:
            delta_t = self.length / prev_speed if prev_speed != 0 else float('inf')
        return delta_t

    @property
    def start_speed(self):
        return self._start_speed

    @property
    def end_speed(self):
        return self._end_speed
    
    @property
    def start_time(self):
        return self._start_time
    
    @property
    def end_time(self):
        return self._end_time

    @property
    def duration_time(self):
        return self._end_time - self._start_time

    def __str__(self):
        return (
            f"Simulated Section from {self._start[0]} º, {self._start[1]} º, {round(self._start[2], 2)} m "
            f"to {self._end[0]} º, {self._end[1]} º, {round(self._end[2], 2)} m\n"
            f"Speeds: {round(self.start_speed, 2)} m/s to {round(self.end_speed, 2)} m/s\n"
            f"Time Elapsed: {round(self.duration_time, 2)} s\n"
            f"Distance: {round(self.length, 2)} m\n"
            f"Total Resistance: {round(self.total_resistance, 2)} N\n"
        )
