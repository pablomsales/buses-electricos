import math

from geopy.distance import geodesic


class Section:
    def __init__(self, coordinates, speeds, timestamps, bus):
        self._coordinates = coordinates
        self._speeds = speeds
        self._timestamps = timestamps

        self.bus = bus

        self.air_density = 1.225

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
    def length(self):
        # obtain latitude & longitude of start coord
        lat_0 = self.start_coord[0]
        long_0 = self.start_coord[1]

        # obtain latitude & longitude of end coord
        lat_1 = self.end_coord[0]
        long_1 = self.end_coord[1]

        # compute the geodesic distance between them in meters
        return geodesic((lat_0, long_0), (lat_1, long_1)).meters

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

    @property
    def duration_time(self):
        x_0, x_1 = 0, self.length
        v_0, v_1 = self.start_speed, self.end_speed
        # despejar t

    @property
    def grade_angle(self):
        delta_altitude = self.end_coord[2] - self.start_coord[2]
        if self.length == 0:
            return 0
        grade_angle = math.degrees(math.atan(delta_altitude / self.length))
        return grade_angle

    def _calculate_average_speed(self):
        return (self.start_speed + self.end_speed) / 2

    def _calculate_acceleration(self):
        delta_v = self.end_speed - self.start_speed
        delta_t = self.end_timestamp - self.start_timestamp
        return delta_v / delta_t if delta_t != 0 else 0

    def _calculate_air_resistance(self):
        return (
            0.5
            * self.air_density
            * self.bus.drag_coefficient
            * self.bus.frontal_area
            * self._average_speed**2
        )

    def _calculate_inertia(self):
        return self.bus.mass * self._acceleration

    def _calculate_grade_resistance(self):
        return self.bus.mass * 9.81 * math.sin(math.radians(self.grade_angle))

    def _calculate_rolling_resistance(self):
        return self.bus.rolling_resistance_coefficient * self.bus.mass * 9.81

    def _calculate_total_resistance(self):
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

    @property
    def total_resistance(self):
        return self._total_resistance

    @property
    def work(self):
        force = self.total_resistance  # (Newtons)
        distance = self.length  # (meters)
        # calculate Work = F·d·cos(θ)
        work = force * distance * math.cos(self.grade_angle)
        return work

    @property
    def instant_power(self):
        # P = E/t
        return self.work / self.duration_time

    def __str__(self):
        return (
            f"\n---------------------------------------------------"
            f"\nSection from {self.start_coord[0]} º, {self.start_coord[1]} º, {round(self.start_coord[2], 2)} m "
            f"to\n{' ' * (len('Section from ')-1)} {self.end_coord[0]} º, {self.end_coord[1]} º, {round(self.end_coord[2], 2)} m"
            f"\n---------------------------------------------------"
            f"\nSpeeds: {round(self.start_speed, 2)} m/s to {round(self.end_speed, 2)} m/s, "
            f"\nTime: {round(self.start_timestamp, 2)} s to {round(self.end_timestamp, 2)} s, "
            f"\nAir Resistance: {self.air_resistance:.2f} N, "
            f"\nInertia: {self.inertia:.2f} N, "
            f"\nGrade Resistance: {self.grade_resistance:.2f} N, "
            f"\nRolling Resistance: {self.rolling_resistance:.2f} N, "
            f"\nTotal Resistance: {self.total_resistance:.2f} N\n"
        )
