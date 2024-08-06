from core.section.base_section import BaseSection


class RealSection(BaseSection):
    def __init__(self, coordinates, speeds, timestamps, bus, emissions):
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
    def duration_time(self):
        return self._end_time - self._start_time
