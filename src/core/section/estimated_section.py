from core.section.base_section import BaseSection


class EstimatedSection(BaseSection):
    def __init__(self, coordinates, bus, emissions):
        super().__init__(coordinates, bus, emissions)

    @property
    def start_speed(self):
        pass

    @property
    def end_speed(self):
        pass

    @property
    def duration_time(self):
        """
        Duration time of the section in seconds.
        """
        # Despejamos el tiempo a partir de las ecuaciones:

        #     v_t = v_0 + a · t
        #     x_t = x_0 + v_0 · t + (1/2 · a · t²)
        x_0, x_t = 0, self.length
        v_0, v_t = self.start_speed, self.end_speed
        # despejar t
        t = (2 * x_t) / (v_0 + v_t)
        return t
