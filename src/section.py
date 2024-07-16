class Section:

    def __init__(self, coordinates, speeds, timestamps):
        self._coordinates = coordinates
        self._speeds = speeds
        self._timestamps = timestamps
        self._motion_resistance = 0

    @property
    def start_coordinates(self):
        return self._coordinates[0]

    @property
    def end_coordinates(self):
        return self._coordinates[1]

    @property
    def start_speed(self):
        return self._speeds[0]

    @property
    def end_speed(self):
        return self._speeds[1]

    def __str__(self):
        return (
            f"Section from {self.start_coordinates} to {self.end_coordinates}, "
            f"Speeds: {self.start_speed} to {self.end_speed}, "
            f"Time: {self._timestamps[0]} to {self._timestamps[1]}"
        )
