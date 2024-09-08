import math

from utils.constants import AIR_DENSITY, GRAVITY


class ResistanceCalculator:
    """
    Calcula las resistencias en una sección de una ruta para un autobús.
    """

    def __init__(self, bus, average_speed, acceleration, grade_angle):
        """
        Inicializa el ResistanceCalculator con un autobús, velocidad promedio, aceleración y ángulo de inclinación.

        Parámetros
        ----------
        bus : Bus
            Instancia de la clase Bus.
        average_speed : float
            Velocidad promedio de la sección en m/s.
        acceleration : float
            Aceleración del autobús en m/s².
        grade_angle : float
            Ángulo de inclinación de la sección en grados.
        """
        self.bus = bus
        self.average_speed = average_speed
        self.acceleration = acceleration
        self.grade_angle = grade_angle

    @property
    def air_resistance(self):
        """
        Calcula la resistencia aerodinámica de la sección.

        Returns
        -------
        float
            Resistencia aerodinámica en Newtons (N).
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
        Calcula la resistencia inercial de la sección.

        Returns
        -------
        float
            Resistencia inercial en Newtons (N).
        """
        return self.bus.total_mass * self.acceleration

    @property
    def grade_resistance(self):
        """
        Calcula la resistencia por inclinación de la sección.

        Returns
        -------
        float
            Resistencia por inclinación en Newtons (N).
        """
        return self.bus.total_mass * GRAVITY * math.sin(math.radians(self.grade_angle))

    @property
    def rolling_resistance(self):
        """
        Calcula la resistencia a la rodadura de la sección.

        Returns
        -------
        float
            Resistencia a la rodadura en Newtons (N).
        """
        return self.bus.rolling_resistance_coefficient * self.bus.total_mass * GRAVITY

    @property
    def total_resistance(self):
        """
        Calcula la resistencia total de la sección.

        Returns
        -------
        float
            Resistencia total en Newtons (N).
        """
        return (
            self.air_resistance
            + self.inertia
            + self.grade_resistance
            + self.rolling_resistance
        )
