from src.models.base_model import BaseModel


class EstimatedModel(BaseModel):
    def __init__(self, filepath, bus, emissions, estimated_speed_func):
        self.estimated_speed_func = estimated_speed_func
        super().__init__(filepath, bus, emissions)

    @property
    def consumption(self):
        return self.route.section.calculate_estimated_consumption(
            self.estimated_speed_func
        )

    @property
    def emissions(self):
        return self.route.section.calculate_estimated_emissions(
            self.estimated_speed_func
        )
