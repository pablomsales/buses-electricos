from src.models.base_model import BaseModel


class RealModel(BaseModel):
    @property
    def consumption(self):
        return self.route.section.calculate_real_consumption()

    @property
    def emissions(self):
        return self.route.section.calculate_real_emissions()
