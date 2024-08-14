from geopy.distance import geodesic
from core.section.base_section import BaseSection

max_acceleration = 0.6  # m/s^2

class SimulatedSection(BaseSection):
    def __init__(self, coordinates, speed_limit, start_speed, start_time, bus, emissions):
        """
        Initialize a SimulatedSection with coordinates, bus, emissions, a single speed limit, 
        start speed, and start time.

        Args:
            coordinates (tuple): A tuple containing start and end coordinates.
            speed_limit (float): Speed limit (km/h) for the section.
            start_speed (float): Speed at the beginning of the section (m/s).
            start_time (float): Time at the beginning of the section (s).
            bus: Instance of the Bus class.
            emissions: Instance of the Emissions class.
        """
        self._speed_limit = speed_limit / 3.6  # Convert km/h to m/s
        self._start_speed = start_speed
        self._start_time = start_time
        self._end_speed = 0.0
        self._end_time = 0.0
        self._start = coordinates[0]  # Coordinates of the start of the section
        self._end = coordinates[1]    # Coordinates of the end of the section
        self.velocities = []          # List of average velocities
        self.start_times = []         # List of start times
        self.end_times = []           # List of end times
        
        # Call base class to initialize necessary attributes
        super().__init__(coordinates, bus, emissions)

    def process(self):
        """Calculate the speed and time for the given section."""
        dist = geodesic(self._start[:2], self._end[:2]).meters
        limit = self._speed_limit
        accel, decel = 0, 0

        if limit == 0:
            self._end_speed = 0
            required_deceleration = (self._start_speed**2) / (2 * dist)
            decel = min(max_acceleration, required_deceleration)
        elif limit < self._start_speed:
            required_deceleration = (self._start_speed**2 - limit**2) / (2 * dist)
            decel = min(max_acceleration, required_deceleration)
            self._end_speed = limit
        elif limit > self._start_speed:
            required_acceleration = (limit**2 - self._start_speed**2) / (2 * dist)
            accel = min(max_acceleration, required_acceleration)
            self._end_speed = limit
        else:
            self._end_speed = limit

        if decel > 0:
            time = (self._start_speed - self._end_speed) / decel
        elif accel > 0:
            time = (self._end_speed - self._start_speed) / accel
        else:
            time = dist / max(self._start_speed, 0.1)

        self._end_time = self._start_time + time  # Calculate end_time
        avg_speed = (self._start_speed + self._end_speed) / 2
        self.velocities.append(avg_speed)
        self.start_times.append(self._start_time)
        self.end_times.append(self._end_time)

    @property
    def start(self) -> tuple[float, float, float]:
        return self._start

    @property
    def end(self) -> tuple[float, float, float]:
        return self._end

    @property
    def start_speed(self):
        return self._start_speed
    
    @start_speed.setter
    def start_speed(self, value):
        self._start_speed = value

    @property
    def end_speed(self):
        return self._end_speed
    
    @end_speed.setter
    def end_speed(self, value):
        self._end_speed = value

    @property
    def start_time(self):
        return self._start_time
    
    @start_time.setter
    def start_time(self, value):
        self._start_time = value

    @property
    def end_time(self):
        return self._end_time
    
    @end_time.setter
    def end_time(self, value):
        self._end_time = value

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
