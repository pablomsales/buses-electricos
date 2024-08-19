from core.section.base_section import BaseSection


class RealSection(BaseSection):
    """
    Class to represent a real section of a route, inheriting from BaseSection.
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
        Initialize a RealSection with coordinates, speeds, timestamps, bus, and emissions.

        Args:
            coordinates (tuple): A tuple containing start and end coordinates.
            speeds (tuple): A tuple containing start and end speeds.
            timestamps (tuple): A tuple containing start and end times.
            bus: Instance of the Bus class.
            emissions: Instance of the Emissions class.
        """
        self._coordinates = coordinates

        self._start_speed = speeds[0]
        self._end_speed = speeds[1]

        self._start_time = timestamps[0]
        self._end_time = timestamps[1]

        super().__init__(coordinates, bus, emissions)

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
    
