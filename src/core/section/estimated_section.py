from core.section import base_section


class EstimatedSection(base_section):
    def __init__(self, coordinates, bus, emissions):
        super().__init__(coordinates, bus, emissions)
