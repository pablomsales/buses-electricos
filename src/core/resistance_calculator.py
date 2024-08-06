import math

from utils.constants import AIR_DENSITY, GRAVITY


class ResistanceCalculator:
    def __init__(self, bus, average_speed, acceleration, grade_angle):
        self.bus = bus
        self.average_speed = average_speed
        self.acceleration = acceleration
        self.grade_angle = grade_angle

    @property
    def air_resistance(self):
        """
        Calculate the air resistance of the section.
        """
        return (
            0.5
            * AIR_DENSITY
            * self.bus.drag_coefficient
            * self.bus.frontal_area
            * self.average_speed**2
        )

    @property
    def inertia(self):
        """
        Calculate the inertia of the section.
        """
        return self.bus.mass * self.acceleration

    @property
    def grade_resistance(self):
        """
        Calculate the grade resistance of the section.
        """
        return self.bus.mass * GRAVITY * math.sin(math.radians(self.grade_angle))

    @property
    def rolling_resistance(self):
        """
        Calculate the rolling resistance of the section.
        """
        return self.bus.rolling_resistance_coefficient * self.bus.mass * GRAVITY

    @property
    def total_resistance(self):
        """
        Calculate the total resistance of the section.
        """
        return (
            self.air_resistance
            + self.inertia
            + self.grade_resistance
            + self.rolling_resistance
        )
