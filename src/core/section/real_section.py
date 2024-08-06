from core.section import base_section


class RealSection(base_section):
    def __init__(self, coordinates, speeds, timestamps, bus, emissions):
        super().__init__(coordinates, bus, emissions)

        self._start_speed = speeds[0]
        self._end_speed = speeds[1]

        self._start_time = timestamps[0]
        self._end_time = timestamps[1]
