import numpy as np
from scipy import constants


class Section:

    def __init__(self, coordinates, speeds, timestamps):
        self._coordinates = coordinates
        self._speeds = speeds
        self._timestamps = timestamps
        self._air_resistance = None
        self._inertia = None
        self._grade_resistance = None
        self._rolling_resistance = None

    @property
    def coord_0(self):
        return self._coordinates[0]

    @property
    def coord_1(self):
        return self._coordinates[1]

    @property
    def velocity_function(self):
        # get start and end speeds & timestamps
        v_0, v_1 = self._speeds[0], self._speeds[1]
        t_0, t_1 = self._timestamps[0], self._timestamps[1]

        # compute gradient & intercept
        m = (v_1 - v_0) / (t_0 - t_1)
        n = v_0 - m * t_0

        return m, n

    @property
    def motion_resistance(self):
        return (
            self._air_resistance
            + self._inertia
            + self._grade_resistance
            + self._rolling_resistance
        )

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

    def compute_air_resistance(self, air_density, drag_coeff, area):
        """
        F = (air_density * drag_coeff * area) / 2 * (self.velocity_function ** 2)
        """
        # resto del codigo aqui

        self._air_resistance = ...
        return self._air_resistance

    def compute_inertia(self, mass):
        """
        F = m * a
        OJO! mass, no weight
        asegurarse de que hay que usar tan solo la aceleracion del vehiculo y
        no la de la gravedad
        """
        acceleration, _ = self.velocity_function

        self._inertia = ...
        return self._inertia

    def compute_grade_resistance(self, mass):
        """
        F = W * sin(theta)
        """
        weight = mass * constants.gravitational_constant
        # sin_theta = z_1 - z_0 ???

        self._grade_resistance = ...
        return self._grade_resistance

    def compute_rolling_resistance(self, mu, mass):
        """
        F = mu * weight

        mu: coefficient of friction
        """
        weight = mass * constants.gravitational_constant

        self._rolling_resistance = ...
        return self._rolling_resistance

    def __str__(self):
        return (
            f"Section from {self.start_coordinates} to {self.end_coordinates}, "
            f"Speeds: {self.start_speed} to {self.end_speed}, "
            f"Time: {self._timestamps[0]} to {self._timestamps[1]}"
        )
