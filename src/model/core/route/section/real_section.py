from core.route.section.base_section import BaseSection

class RealSection(BaseSection):
    """
    Clase para representar una sección real de una ruta, heredando de BaseSection.
    """

    def __init__(
        self,
        coordinates: tuple[tuple[float, float, float], tuple[float, float, float]],
        speeds: tuple[float, float],
        timestamps: tuple[float, float],
        bus,
        emissions,
    ):
        """
        Inicializa una RealSection con coordenadas, velocidades, marcas de tiempo, un bus y emisiones.

        Args:
            coordinates (tuple): Una tupla que contiene coordenadas de inicio y fin.
            speeds (tuple): Una tupla que contiene las velocidades de inicio y fin.
            timestamps (tuple): Una tupla que contiene los tiempos de inicio y fin.
            bus: Instancia de la clase Bus.
            emissions: Instancia de la clase Emissions.
        """
        self._coordinates = coordinates
        self._start_speed = speeds[0]
        self._end_speed = speeds[1]
        self._start_time = timestamps[0]
        self._end_time = timestamps[1]

        super().__init__(coordinates, bus, emissions)

    @property
    def start_speed(self):
        """
        Obtiene la velocidad de inicio de la sección.

        Returns:
            float: Velocidad de inicio en m/s.
        """
        return self._start_speed

    @property
    def end_speed(self):
        """
        Obtiene la velocidad de fin de la sección.

        Returns:
            float: Velocidad de fin en m/s.
        """
        return self._end_speed
    
    @property
    def start_time(self):
        """
        Obtiene el tiempo de inicio de la sección.

        Returns:
            float: Tiempo de inicio en segundos.
        """
        return self._start_time
    
    @property
    def end_time(self):
        """
        Obtiene el tiempo de fin de la sección.

        Returns:
            float: Tiempo de fin en segundos.
        """
        return self._end_time
