class ChargingPoint:
    """
    Class to represent a charging point.
    """
    def __init__(self, id, bus, coordinates, max_power, distance, time):
        """
        Initialize a ChargingPoint instance.

        Parameters
        ----------
        id : int
            Unique identifier for the charging point.
        bus : Bus
            The bus instance that will be charged.
        coordinates : tuple
            Represents the coordinates of the charging point.
        max_power : float
            Maximum power output of the charging point in kW.
        distance : float
            Distance from the last point of the route to the charging point in kilometres.
        time : float
            Time from the last point of the route to the charging point in minutes.
        """
        self.id = id
        self._bus = bus
        self.coordinates = coordinates
        self.max_power = max_power
        self.distance = distance # kilometres
        self.time = time # minutes

    def cost(self):
        """
        Calculate the cost (electric consumption) of driving to the charging point.

        Returns
        -------
        tuple
            Tuple containing the electric consumption in Wh and Ah.
        """
        power = self._bus.engine.max_power
        hours = self.time / 60 # convert minutes to hours
        voltage = self._bus.engine.battery.voltage_v

        # Compute consumption in Wh and Ah
        watts_hour = power * hours
        ampers_hour = watts_hour / voltage

        return watts_hour, ampers_hour


    def __str__(self):
        return f"ChargingPoint {self.id} at {self.location} with max power {self.max_power} kW, at {self.time} minutes and {self.distance} km away"