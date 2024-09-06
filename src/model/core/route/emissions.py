from utils.constants import CO2_CONVERSION_FACTOR, euro_standards


class Emissions:
    """
    Class to calculate emissions based on the EURO standard.
    """

    def __init__(self, euro_standard: str, electric: bool):
        """
        Initialize an Emissions instance with the EURO standard.

        Parameters
        ----------
        euro_standard : str
            The EURO standard for emissions.
        """

        self._validate_euro_standard(euro_standard)
        self.euro_standard = euro_standard
        self.standards = euro_standards[euro_standard]
        self._electric = electric

    @staticmethod
    def _validate_euro_standard(euro_standard):
        if euro_standard not in euro_standards:
            raise ValueError(f"Invalid EURO standard: {euro_standard}")

    def calculate_emissions(self, power_kw, fuel_consumption_rate):
        """
        Calculate emissions based on the given power in kW.
        Returns a dictionary with the emissions for NOx, CO, HC, PM, and CO2 in grams per second.
        """
        # Si el vehículo es eléctrico, todas las emisiones son cero
        if self._electric:
            return {"NOx": 0, "CO": 0, "HC": 0, "PM": 0, "CO2": 0}

        emissions = self._calculate_pollutant_emissions(power_kw)

        # Add CO2 emissions
        if fuel_consumption_rate != 0:
            emissions["CO2"] = self._calculate_co2_emissions(fuel_consumption_rate)
        else:
            emissions["CO2"] = 0

        return emissions

    def _calculate_pollutant_emissions(self, power_kw):
        """
        Calculate emissions for NOx, CO, HC, and PM based on the given power in kW.
        """
        # Si el vehículo es eléctrico, todas las emisiones son cero
        if self._electric:
            return {"NOx": 0, "CO": 0, "HC": 0, "PM": 0}

        # Si la potencia del motor es negativa, la ajustamos para evitar valores inválidos.
        if power_kw < 0:
            if self._electric:
                power_kw = 0
            else:
                # NOTE: Para motores de combustión interna, se puede considerar una constante
                # para representar el motor en ralentí. Por simplicidad, la ajustamos a 0.
                # En el futuro, se debe modificar este valor para reflejar mejor el ralenti.
                power_kw = 0

        return {
            pollutant: value * power_kw / 3600  # converting g/kWh to g/s
            for pollutant, value in self.standards.items()
        }

    def _calculate_co2_emissions(self, fuel_consumption_rate):
        """
        Calculate CO2 emissions based on the fuel consumption rate in liters per second.
        """
        co2_kg_per_second = fuel_consumption_rate * CO2_CONVERSION_FACTOR
        co2_g_per_second = co2_kg_per_second * 1000
        return co2_g_per_second

    def __str__(self):
        return f"Emissions Standards: {self.euro_standard}\n" + "\n".join(
            [f"{k}: {v} g/kWh" for k, v in self.standards.items()]
        )
