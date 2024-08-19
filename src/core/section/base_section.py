import math

from geopy.distance import geodesic

from core.resistance_calculator import ResistanceCalculator


class BaseSection:
    """
    Class to represent a section of a route.
    """

    def __init__(self, coordinates, bus, emissions):
        """
        Initialize a BaseSection with coordinates, bus, and emissions.

        Args:
            coordinates (tuple): A tuple containing 2 tuple: start and end coordinates.
            bus: Instance of the Bus class.
            emissions: Instance of the Emissions class.
        """
        self._start = coordinates[0]  # Coordinates for the start of the section
        self._end = coordinates[1]  # Coordinates for the end of the section

        self.bus = bus
        self.emissions = emissions

        self._average_speed = self._calculate_average_speed()
        self._acceleration = self._calculate_acceleration()
        self._grade_angle = self.grade_angle

        self.resistance_calculator = ResistanceCalculator(
            self.bus,
            self._average_speed,
            self._acceleration,
            self._grade_angle,
        )

    @property
    def start(self) -> tuple[float, float, float]:
        return self._start

    @property
    def end(self) -> tuple[float, float, float]:
        return self._end

    @property
    def length(self) -> float:
        """
        Length of the section in meters.
        Computes the length using the geodesic distance
        """

        # obtain latitude & longitude of start coord
        lat_0, long_0 = self.start[0], self.start[1]
        # obtain latitude & longitude of end coord
        lat_1, long_1 = self.end[0], self.end[1]

        # compute the geodesic distance between them in meters
        return geodesic((lat_0, long_0), (lat_1, long_1)).meters

    @property
    def grade_angle(self) -> float:
        """
        Grade angle of the section in degrees.
        """
        delta_altitude = self.end[2] - self.start[2]
        return (
            math.degrees(math.atan(delta_altitude / self.length))
            if self.length != 0
            else 0
        )

    def _calculate_average_speed(self) -> float:
        """
        Calculate the average speed of the section.
        """
        return (self.start_speed + self.end_speed) / 2

    def _calculate_acceleration(self) -> float:
        """
        Calculate the constant acceleration of the section.
        """
        delta_v = self.end_speed - self.start_speed
        delta_t = self.duration_time
        return delta_v / delta_t if delta_t != 0 else 0

    @property
    def air_resistance(self) -> float:
        return self.resistance_calculator.air_resistance

    @property
    def inertia(self) -> float:
        return self.resistance_calculator.inertia

    @property
    def grade_resistance(self) -> float:
        return self.resistance_calculator.grade_resistance

    @property
    def rolling_resistance(self) -> float:
        return self.resistance_calculator.rolling_resistance

    @property
    def total_resistance(self) -> float:
        return self.resistance_calculator.total_resistance

    @property
    def work(self) -> float:
        """
        Work (J) done in the section.
        """
        force = self.total_resistance  # (Newtons)
        distance = self.length  # (meters)
        return force * distance * math.cos(math.radians(self.grade_angle))

    @property
    def instant_power(self) -> float:
        """
        Instantaneous power in the section in Watts.
        """
        return self.work / self.duration_time  # Watts

    @property
    def consumption(self) -> dict[str, float]:
        """
        Calculate the consumption of the section.
        Returns:
            dict: A dictionary with consumption values.
        """
        return self.bus.engine.consumption(
            power=self.instant_power,
            time=self.duration_time,
            km=self.length / 1000,
        )

    @property
    def section_emissions(self) -> dict[str, float]:
        """
        Calculate emissions of the section.

        Returns:
            dict: A dictionary with emission values in grams per second.
        """

        power_kw = self.instant_power / 1000  # Convert W to kW

        # gonna be 0 when ElectricalEngine, so will not interfere
        fuel_consumption_rate = self.consumption["L/km"] / self.duration_time

        return self.emissions.calculate_emissions(
            power_kw,
            fuel_consumption_rate=fuel_consumption_rate,
        )

    def get_battery_degradation_in_section(self):
        return self.bus.get_battery_degradation_in_section()

    def get_battery_state_of_charge(self):
        return self.bus.get_battery_state_of_charge()

    def get_battery_depth_of_discharge(self):
        return self.bus.get_battery_depth_of_discharge()

    def __str__(self):
        emissions_str = "\n".join(
            [f"{k}: {v:.6f} g/s" for k, v in self.section_emissions.items()]
        )

        return (
            f"\n---------------------------------------------------"
            f"\nSection from {self.start[0]} º, {self.start[1]} º, {round(self.start[2], 2)} m "
            f"to\n{' ' * (len('Section from ')-1)} {self.end[0]} º, {self.end[1]} º, {round(self.end[2], 2)} m"
            f"\n---------------------------------------------------"
            f"\nSpeeds: {round(self.start_speed, 2)} m/s to {round(self.end_speed, 2)} m/s, "
            f"\nAir Resistance: {self.air_resistance:.2f} N, "
            f"\nInertia: {self.inertia:.2f} N, "
            f"\nGrade Resistance: {self.grade_resistance:.2f} N, "
            f"\nRolling Resistance: {self.rolling_resistance:.2f} N, "
            f"\nTotal Resistance: {self.total_resistance:.2f} N\n"
            f"\nWork: {self.work:.2f} J"
            f"\nRequired Power: {self.instant_power:.2f} W"
            f"\nConsumption: {self.consumption}"
            f"\n\nEmissions:\n{emissions_str}"
            f"\n\nBattery SoC: {self.get_battery_state_of_charge()}"
            f"\nBattery degradation:{self.get_battery_degradation_in_section()}"
            f"\nBattery DoD (Health): {self.get_battery_depth_of_discharge()}"
            f"\n"
        )
