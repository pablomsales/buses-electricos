from src.core.section import BaseSection


class EstimatedSection(BaseSection):
    def __init__(self, coordinates, bus, emissions):
        super().__init__(coordinates, bus, emissions)
