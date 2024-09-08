class ChargingPoint:
    """
    Clase para representar un punto de carga.
    """
    def __init__(self, id, bus, coordinates, max_power, distance, time):
        """
        Inicializa una instancia de ChargingPoint.

        Parámetros
        ----------
        id : int
            Identificador único para el punto de carga.
        bus : Bus
            La instancia del autobús que será cargado.
        coordinates : tuple
            Representa las coordenadas del punto de carga.
        max_power : float
            Potencia máxima de salida del punto de carga en kW.
        distance : float
            Distancia desde el último punto de la ruta hasta el punto de carga en kilómetros.
        time : float
            Tiempo desde el último punto de la ruta hasta el punto de carga en minutos.
        """
        self.id = id
        self._bus = bus
        self.coordinates = coordinates
        self.max_power = max_power
        self.distance = distance # kilómetros
        self.time = time # minutos

    def cost(self):
        """
        Calcula el costo (consumo eléctrico) de conducir hasta el punto de carga.

        Returns
        -------
        tuple
            Tupla que contiene el consumo eléctrico en Wh y Ah.
        """
        power = self._bus.engine.max_power
        hours = self.time / 60 # convertir minutos a horas
        voltage = self._bus.engine.battery.voltage_v

        # Calcular el consumo en Wh y Ah
        watts_hour = power * hours
        ampers_hour = watts_hour / voltage

        return watts_hour, ampers_hour

    def __str__(self):
        return f"Punto de carga {self.id} en {self.coordinates} con potencia máxima de {self.max_power} kW, a {self.time} minutos y {self.distance} km de distancia"
