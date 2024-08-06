import math

from geopy.distance import geodesic


class Section:
    """
    Class to represent a section of a route.
    """

    def __init__(self, coordinates, bus, emissions):
        self._start = coordinates[0]
        self._end = coordinates[1]

        self.bus = bus
        self.emissions = emissions

        self.air_density = 1.225

        self._average_speed = self._calculate_average_speed()
        self._acceleration = self._calculate_acceleration()

        self._air_resistance = self._calculate_air_resistance()
        self._inertia = self._calculate_inertia()
        self._grade_resistance = self._calculate_grade_resistance()
        self._rolling_resistance = self._calculate_rolling_resistance()

        self._total_resistance = self._calculate_total_resistance()

    @property
    def start(self):
        return self._coordinates[0]

    @property
    def end(self):
        return self._coordinates[1]

    @property
    def length(self):
        """
        Length of the section in meters.
        """
        # obtain latitude & longitude of start coord
        lat_0 = self.start[0]
        long_0 = self.start[1]

        # obtain latitude & longitude of end coord
        lat_1 = self.end[0]
        long_1 = self.end[1]

        # compute the geodesic distance between them in meters
        return geodesic((lat_0, long_0), (lat_1, long_1)).meters

    @property
    def grade_angle(self):
        """
        Grade angle of the section in degrees.
        """
        delta_altitude = self.end[2] - self.start[2]
        if self.length == 0:
            return 0
        return math.degrees(math.atan(delta_altitude / self.length))

    def _calculate_average_speed(self):
        """
        Calculate the average speed of the section.
        """
        return (self.start_speed + self.end_speed) / 2

    def _calculate_acceleration(self):
        """
        Calculate the acceleration of the section.
        """
        delta_v = self.end_speed - self.start_speed
        delta_t = self.end_timestamp - self.start_timestamp
        return delta_v / delta_t if delta_t != 0 else 0

    def _calculate_air_resistance(self):
        """
        Calculate the air resistance of the section.
        """
        return (
            0.5
            * self.air_density
            * self.bus.drag_coefficient
            * self.bus.frontal_area
            * self._average_speed**2
        )

    def _calculate_inertia(self):
        """
        Calculate the inertia of the section.
        """
        return self.bus.mass * self._acceleration

    def _calculate_grade_resistance(self):
        """
        Calculate the grade resistance of the section.
        """
        return self.bus.mass * 9.81 * math.sin(math.radians(self.grade_angle))

    def _calculate_rolling_resistance(self):
        """
        Calculate the rolling resistance of the section.
        """
        return self.bus.rolling_resistance_coefficient * self.bus.mass * 9.81

    def _calculate_total_resistance(self):
        """
        Calculate the total resistance of the section.
        """
        return (
            self._air_resistance
            + self._inertia
            + self._grade_resistance
            + self._rolling_resistance
        )

    @property
    def air_resistance(self):
        """
        Air resistance of the section.
        """
        return self._air_resistance

    @property
    def inertia(self):
        """
        Inertia of the section.
        """
        return self._inertia

    @property
    def grade_resistance(self):
        """
        Grade resistance of the section.
        """
        return self._grade_resistance

    @property
    def rolling_resistance(self):
        """
        Rolling resistance of the section.
        """
        return self._rolling_resistance

    @property
    def total_resistance(self):
        """
        Total resistance of the section.
        """
        return self._total_resistance

    @property
    def work(self):
        """
        Work done in the section.
        """
        force = self.total_resistance  # (Newtons)
        distance = self.length  # (meters)
        return force * distance * math.cos(math.radians(self.grade_angle))

    @property
    def instant_power(self):
        """
        Instantaneous power in the section in Watts.
        """
        return self.work / self.duration_time  # Watts

    @property
    def consumption(self):
        """
        Consumption of the section.
        """
        if self.bus.engine.engine_type == "electric":
            return self.bus.engine.consumption(
                power=self.instant_power,
                time=self.duration_time,
            )
        else:
            # if engine_type is "combustion", include km in consumption
            kilometers = self.length / 1000
            return self.bus.engine.consumption(
                power=self.instant_power,
                time=self.duration_time,
                kilometers=kilometers,
            )

    @property
    def section_emissions(self):
        """
        Emissions of the section.
        """
        power_kw = self.instant_power / 1000  # Convertir W a kW

        if self.bus.engine.engine_type == "electric":
            return self.emissions.calculate_emissions(power_kw)
        else:
            # first get the litres consumed in 1 second
            litres_per_second = self.consumption / self.duration_time
            # get emissions including the L/s
            return self.emissions.calculate_emissions(
                power_kw, fuel_litres_per_second=litres_per_second
            )

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
            f"\nConsumption: {self.consumption} {self.bus.engine.consumption_units}"
            f"\n\nEmissions:\n{emissions_str}"
            f"\n\nSection.duration_time():\t{self.duration_time}"
            f"\n"
        )
