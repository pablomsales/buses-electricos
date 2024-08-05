from utils.constants import euro_standards


class Emissions:
    """
    Class to calculate emissions based on the EURO standard.
    """

    def __init__(self, euro_standard):
        if euro_standard not in euro_standards:
            raise ValueError(f"Invalid EURO standard: {euro_standard}")
        self.euro_standard = euro_standard
        self.standards = euro_standards[euro_standard]

    def calculate_emissions(self, power_kw, fuel_litres_per_second=None):
        """
        Calculate emissions based on the given power in kW.
        Returns a dictionary with the emissions for NOx, CO, HC, and PM in grams per second.
        """
        emissions = {}
        for pollutant, value in self.standards.items():
            emissions[pollutant] = value * power_kw / 3600  # converting g/kWh to g/s

        if fuel_litres_per_second:
            # add CO2 emissions
            # 1L gasoil --> 2.64kg CO2
            co2_kg = fuel_litres_per_second * 2.64
            co2_g = co2_kg * 1000
            emissions["CO2"] = co2_g

        return emissions

    def __str__(self):
        return f"Emissions Standards: {self.euro_standard}\n" + "\n".join(
            [f"{k}: {v} g/kWh" for k, v in self.standards.items()]
        )
