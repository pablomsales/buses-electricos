import math


class Section:

    def __init__(self, coordinates, speeds, timestamps, mass, drag_coefficient, frontal_area, rolling_resistance_coefficient, grade_angle):
        self._coordinates = coordinates
        self._speeds = speeds
        self._timestamps = timestamps
        self.mass = mass
        self.drag_coefficient = drag_coefficient
        self.frontal_area = frontal_area
        self.rolling_resistance_coefficient = rolling_resistance_coefficient
        self.air_density = 1.225  # kg/m^3, density of air at sea level
        self.gravity = 9.81  # m/s^2, acceleration due to gravity
        self.grade_angle = grade_angle

        # We calculate the immutable properties of the section
        self._average_speed = self._calculate_average_speed()
        self._acceleration = self._calculate_acceleration()

        self._air_resistance = self._calculate_air_resistance()
        self._inertia = self._calculate_inertia()
        self._grade_resistance = self._calculate_grade_resistance()
        self._rolling_resistance = self._calculate_rolling_resistance()
        
        self._total_resistance = self._calculate_total_resistance()

    @property
    def start_coord(self):
        return self._coordinates[0]

    @property
    def end_coord(self):
        return self._coordinates[1]

    @property
    def start_speed(self):
        return self._speeds[0]

    @property
    def end_speed(self):
        return self._speeds[1]

    @property
    def start_timestamp(self):
        return self._timestamps[0]

    @property
    def end_timestamp(self):
        return self._timestamps[1]
    
    def _calculate_average_speed(self):
        return (self.start_speed + self.end_speed) / 2
    
    def _calculate_acceleration(self):
        delta_v = self.end_speed - self.start_speed
        delta_t = self.end_timestamp - self.start_timestamp
        return delta_v / delta_t if delta_t != 0 else 0

    def _calculate_air_resistance(self):
        return 0.5 * self.air_density * self.drag_coefficient * self.frontal_area * self._average_speed ** 2
    
    def _calculate_inertia(self):
        return self.mass * self._acceleration
    
    def _calculate_grade_resistance(self):
        return self.mass * self.gravity * math.sin(math.radians(self.grade_angle))
    
    def _calculate_rolling_resistance(self):
        return self.rolling_resistance_coefficient * self.mass * self.gravity
    
    def _calculate_total_resistance(self):
        return (self._air_resistance +
                self._inertia +
                self._grade_resistance +
                self._rolling_resistance)
    
    @property
    def air_resistance(self):
        return self._air_resistance
    
    @property
    def inertia(self):
        return self._inertia
    
    @property
    def grade_resistance(self):
        return self._grade_resistance
    
    @property
    def rolling_resistance(self):
        return self._rolling_resistance
    
    @property
    def total_resistance(self):
        return self._total_resistance

    def __str__(self):
        return (
            f"Section from {self.start_coord} to {self.end_coord}, "
            f"Speeds: {self.start_speed} to {self.end_speed}, "
            f"Time: {self.start_timestamp} to {self.end_timestamp}, "
            f"Air Resistance: {self.air_resistance:.2f} N, "
            f"Inertia: {self.inertia:.2f} N, "
            f"Grade Resistance: {self.grade_resistance:.2f} N, "
            f"Rolling Resistance: {self.rolling_resistance:.2f} N, "
            f"Total Resistance: {self.total_resistance:.2f} N"
        )