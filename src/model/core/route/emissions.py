from utils.constants import CO2_CONVERSION_FACTOR, euro_standards


class Emissions:
    """
    Clase para calcular las emisiones basadas en el estándar EURO.
    """

    def __init__(self, euro_standard: str, electric: bool):
        """
        Inicializa una instancia de Emissions con el estándar EURO.

        Parámetros
        ----------
        euro_standard : str
            El estándar EURO para las emisiones.
        electric : bool
            Indica si el vehículo es eléctrico.
        """
        self._validate_euro_standard(euro_standard)
        self.euro_standard = euro_standard
        self.standards = euro_standards[euro_standard]
        self._electric = electric

    @staticmethod
    def _validate_euro_standard(euro_standard):
        if euro_standard not in euro_standards:
            raise ValueError(f"Estándar EURO inválido: {euro_standard}")

    def calculate_emissions(self, power_kw, fuel_consumption_rate):
        """
        Calcula las emisiones basadas en la potencia dada en kW.

        Parámetros
        ----------
        power_kw : float
            La potencia en kW.
        fuel_consumption_rate : float
            La tasa de consumo de combustible en litros por segundo.

        Returns
        -------
        dict
            Un diccionario con las emisiones para NOx, CO, HC, PM y CO2 en gramos por segundo.
        """
        # Si el vehículo es eléctrico, todas las emisiones son cero
        if self._electric:
            return {"NOx": 0, "CO": 0, "HC": 0, "PM": 0, "CO2": 0}

        emissions = self._calculate_pollutant_emissions(power_kw)

        # Agregar emisiones de CO2
        if fuel_consumption_rate != 0:
            emissions["CO2"] = self._calculate_co2_emissions(fuel_consumption_rate)
        else:
            emissions["CO2"] = 0

        return emissions

    def _calculate_pollutant_emissions(self, power_kw):
        """
        Calcula las emisiones de NOx, CO, HC y PM basadas en la potencia dada en kW.

        Parámetros
        ----------
        power_kw : float
            La potencia en kW.

        Returns
        -------
        dict
            Un diccionario con las emisiones para NOx, CO, HC y PM en gramos por segundo.
        """
        # Si el vehículo es eléctrico, todas las emisiones son cero
        if self._electric:
            return {"NOx": 0, "CO": 0, "HC": 0, "PM": 0}

        # Ajustar potencia negativa
        if power_kw < 0:
            if self._electric:
                power_kw = 0
            else:
                power_kw = 0  # Ajuste simplificado para motores en ralentí

        return {
            pollutant: value * power_kw / 3600  # convertir g/kWh a g/s
            for pollutant, value in self.standards.items()
        }

    def _calculate_co2_emissions(self, fuel_consumption_rate):
        """
        Calcula las emisiones de CO2 basadas en la tasa de consumo de combustible en litros por segundo.

        Parámetros
        ----------
        fuel_consumption_rate : float
            La tasa de consumo de combustible en litros por segundo.

        Returns
        -------
        float
            Emisiones de CO2 en gramos por segundo.
        """
        co2_kg_per_second = fuel_consumption_rate * CO2_CONVERSION_FACTOR
        co2_g_per_second = co2_kg_per_second * 1000
        return co2_g_per_second

    def __str__(self):
        return f"Estándares de Emisiones: {self.euro_standard}\n" + "\n".join(
            [f"{k}: {v} g/kWh" for k, v in self.standards.items()]
        )
