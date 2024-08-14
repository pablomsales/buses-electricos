import math
from core.section.base_section import BaseSection

ACCELERATION_LIMIT = 0.6  # m/s^2
DECELERATION_LIMIT = -0.6  # m/s^2

class SimulatedSection(BaseSection):
    def __init__(self, coordinates, bus, emissions, speed_limit):
        """
        Initialize a SimulatedSection with coordinates, bus, emissions, and a single speed limit.

        Args:
            coordinates (tuple): A tuple containing start and end coordinates.
            bus: Instance of the Bus class.
            emissions: Instance of the Emissions class.
            speed_limit (float): Speed limit (m/s) for the section.
        """
        self._speed_limit = speed_limit / 3.6  # km/h to m/s
        self._start_speed = 0.0
        self._end_speed = None
        self._start_time = 0.0
        self._end_time = None
        self._start = coordinates[0]  # Coordinates for the start of the section
        self._end = coordinates[1]  # Coordinates for the end of the section
        super().__init__(coordinates, bus, emissions)

    def simulate(self, prev_speed):
        """
        Simulate the section by calculating the speed and time based on the speed limit and distance.

        Args:
            prev_speed (float): Speed at the start of the section (from previous section).
        """
        current_speed = prev_speed

        # Calculate acceleration and final speed
        acceleration, final_speed = self.calculate_acceleration(current_speed, self._speed_limit, self.length)

        # Calculate time to travel the section
        time_to_travel = self.calculate_time(acceleration, current_speed)
        self._end_time = self._start_time + time_to_travel

        # Update the speed at the end of the section
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

        # Calculate the achievable speed at the end of the section
        achievable_speed = math.sqrt(max(prev_speed**2 + 2 * (acceleration + total_resistance) * distance, 0))
        return acceleration, achievable_speed

    def calculate_time(self, acceleration, prev_speed):
        """
        Calculate the time needed to travel the section.

        Args:
            acceleration (float): Constant acceleration in m/s^2.
            prev_speed (float): Initial speed in m/s.

        Returns:
            float: Time needed in seconds.
        """
        if acceleration != 0:
            delta_t = (self._end_speed - prev_speed) / acceleration
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
    def duration_time(self):
        return self._end_time - self._start_time

    def __str__(self):
        return (
            f"Simulated Section from {self.start[0]} º, {self.start[1]} º, {round(self.start[2], 2)} m "
            f"to {self.end[0]} º, {self.end[1]} º, {round(self.end[2], 2)} m\n"
            f"Speeds: {round(self.start_speed, 2)} m/s to {round(self.end_speed, 2)} m/s\n"
            f"Time Elapsed: {round(self.duration_time, 2)} s\n"
            f"Distance: {round(self.length, 2)} m\n"
            f"Total Resistance: {round(self.total_resistance, 2)} N\n"
        )
