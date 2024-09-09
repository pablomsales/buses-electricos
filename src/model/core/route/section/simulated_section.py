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


from core.route.section.base_section import BaseSection
from utils.constants import MAX_ACCELERATION, MAX_DECELERATION

class SimulatedSection(BaseSection):
    """
    Representa una sección de una ruta que ha sido simulada.
    """

    def __init__(
        self, coordinates, speed_limit, start_speed, start_time, bus, emissions
    ):
        """
        Inicializa una SimulatedSection con coordenadas, un límite de velocidad, velocidad de inicio,
        y tiempo de inicio.

        Args:
            coordinates (tuple): Una tupla que contiene coordenadas de inicio y fin.
            speed_limit (float): Límite de velocidad (km/h) para la sección.
            start_speed (float): Velocidad al comienzo de la sección (m/s).
            start_time (float): Tiempo al comienzo de la sección (s).
            bus: Instancia de la clase Bus.
            emissions: Instancia de la clase Emissions.
        """
        self._speed_limit = speed_limit / 3.6  # Convertir km/h a m/s
        self._start_speed = start_speed
        self._start_time = start_time
        self._end_speed = 0.0
        self._end_time = 0.0
        self.velocities = []  # Lista de velocidades promedio
        self.start_times = []  # Lista de tiempos de inicio
        self.end_times = []  # Lista de tiempos de fin

        # Llamar a la clase base para inicializar atributos necesarios
        super().__init__(coordinates, bus, emissions)

        # Procesar la sección
        self._process()

    def _process(self):
        """Calcula la velocidad y el tiempo para la sección dada considerando la resistencia total."""
        dist = self.length  # Distancia de la sección
        limit = self._speed_limit

        # Calcular la aceleración y desaceleración efectivas basadas en la resistencia total
        effective_max_acceleration, effective_max_deceleration = (
            self._calculate_effective_forces()
        )

        # Calcular la velocidad final basada en el límite de velocidad y la velocidad de inicio
        self._end_speed, decel, accel = self._calculate_end_speed(
            limit, dist, effective_max_acceleration, effective_max_deceleration
        )

        self._acceleration = self._set_acceleration(decel, accel)

        # Calcular el tiempo requerido para atravesar la sección
        self._end_time = self._calculate_time(decel, accel, dist)

        # Calcular y almacenar la velocidad promedio
        avg_speed = self._calculate_average_speed()
        self.velocities.append(avg_speed)
        self.start_times.append(self._start_time)
        self.end_times.append(self._end_time)

    def _calculate_effective_forces(self):
        """Calcula la aceleración y desaceleración efectivas basadas en la resistencia total."""
        total_resistance = self.total_resistance  # N
        effective_max_acceleration = MAX_ACCELERATION - (
            total_resistance / self.bus.total_mass
        )
        effective_max_deceleration = MAX_DECELERATION + (
            total_resistance / self.bus.total_mass
        )
        return effective_max_acceleration, effective_max_deceleration

    def _decelerate_to_stop(self, dist, effective_max_deceleration, step_size=1.0):
        """Maneja el caso donde la velocidad debe reducirse a cero reduciendo la velocidad inicial
        mientras que la desaceleración calculada es mayor que la desaceleración máxima permitida.
        """
        self._end_speed = 0
        decel = self._calculate_instant_acceleration(
            self._start_speed, self._end_speed, dist
        )
        while abs(decel) > abs(effective_max_deceleration):
            if self._start_speed - step_size >= 0:
                self._start_speed -= step_size
            decel = (-self._start_speed**2) / (2 * dist)
        return decel, None

    def _decelerate(self, limit, dist, effective_max_deceleration, step_size=1.0):
        """Maneja el caso donde la velocidad debe reducirse a un cierto límite reduciendo la velocidad
        inicial mientras que la desaceleración calculada es mayor que la desaceleración máxima permitida.
        """
        self._end_speed = limit
        decel = self._calculate_instant_acceleration(
            self._start_speed, self._end_speed, dist
        )
        while abs(decel) > abs(effective_max_deceleration):
            if self._end_speed - step_size >= 0:
                self._end_speed -= step_size
            if self._start_speed - step_size >= 0:
                self._start_speed -= step_size
            decel = (self._end_speed**2 - self._start_speed**2) / (2 * dist)
        return decel, None

    def _accelerate(self, limit, dist, effective_max_acceleration, step_size=1.0):
        """Maneja el caso donde la velocidad debe aumentarse a un cierto límite acelerando la cantidad
        necesaria si la aceleración calculada está por debajo de la aceleración máxima permitida. De lo contrario,
        la velocidad se reduce hasta que la aceleración esté por debajo del límite máximo permitido.
        """
        self._end_speed = limit
        accel = self._calculate_instant_acceleration(
            self._start_speed, self._end_speed, dist
        )
        while abs(accel) > abs(effective_max_acceleration):
            if self._end_speed - step_size >= 0:
                self._end_speed -= step_size
            if self._start_speed - step_size >= 0:
                self._start_speed -= step_size
            accel = (self._end_speed**2 - self._start_speed**2) / (2 * dist)
        return None, accel

    def _calculate_end_speed(
        self, limit, dist, effective_max_acceleration, effective_max_deceleration
    ):
        """Determina la velocidad final y la posible aceleración o desaceleración."""
        if limit == 0:
            decel, accel = self._decelerate_to_stop(dist, effective_max_deceleration)
        elif limit < self._start_speed:
            decel, accel = self._decelerate(limit, dist, effective_max_deceleration)
        elif limit > self._start_speed:
            decel, accel = self._accelerate(limit, dist, effective_max_acceleration)
        else:
            self._end_speed = limit
            decel, accel = None, None

        # Retornar la velocidad final, desaceleración y aceleración
        return self._end_speed, decel, accel

    def _calculate_instant_acceleration(self, start_speed, end_speed, dist):
        """Calcula la aceleración instantánea para la sección."""
        return (end_speed**2 - start_speed**2) / (2 * dist)

    def _set_acceleration(self, decel, accel):
        """Establece la aceleración basada en los valores de desaceleración y aceleración."""
        if accel is not None and decel is None:
            return accel
        elif decel is not None and accel is None:
            return decel
        else:
            return 0.0

    def _calculate_time(self, decel, accel, dist):
        """Calcula el tiempo requerido para atravesar la sección."""
        if decel is not None and decel < 0:
            time = (self._start_speed - self._end_speed) / abs(
                decel
            )  # t = (vi - vf) / |a|
        elif accel is not None and accel > 0:
            time = (self._end_speed - self._start_speed) / accel
        else:
            time = dist / max(self._start_speed, 0.1)

        return self._start_time + time

    @property
    def acceleration(self):
        """
        Obtiene la aceleración de la sección.

        Returns:
            float: Aceleración en m/s².
        """
        return self._acceleration

    @acceleration.setter
    def acceleration(self, value):
        self._acceleration = value

    @property
    def start_speed(self):
        """
        Obtiene la velocidad de inicio de la sección.

        Returns:
            float: Velocidad de inicio en m/s.
        """
        return self._start_speed

    @start_speed.setter
    def start_speed(self, value):
        self._start_speed = value

    @property
    def end_speed(self):
        """
        Obtiene la velocidad final de la sección.

        Returns:
            float: Velocidad final en m/s.
        """
        return self._end_speed

    @end_speed.setter
    def end_speed(self, value):
        self._end_speed = value

    @property
    def start_time(self):
        """
        Obtiene el tiempo de inicio de la sección.

        Returns:
            float: Tiempo de inicio en segundos.
        """
        return self._start_time

    @start_time.setter
    def start_time(self, value):
        self._start_time = value

    @property
    def end_time(self):
        """
        Obtiene el tiempo final de la sección.

        Returns:
            float: Tiempo final en segundos.
        """
        return self._end_time

    @end_time.setter
    def end_time(self, value):
        self._end_time = value

    def __str__(self):
        return (
            f"Sección simulada desde {self._start[0]} º, {self._start[1]} º, {round(self._start[2], 2)} m "
            f"hacia {self._end[0]} º, {self._end[1]} º, {round(self._end[2], 2)} m\n"
            f"Velocidades: {round(self.start_speed, 2)} m/s a {round(self.end_speed, 2)} m/s\n"
            f"Tiempo transcurrido: {round(self.duration_time, 2)} s\n"
            f"Distancia: {round(self.length, 2)} m\n"
            f"Resistencia total: {round(self.total_resistance, 2)} N\n"
            f"Aceleración/Desaceleración calculada: {round(self.acceleration, 2)} m/s²\n"
        )
