class Fuel:
    """
    Class representing a fuel type.
    """

    _fuels_lhv = {
        "gasoline": 3.1536e7,  # J/L
        "diesel": 3.58e7,  # J/L
        "propane": 2.5e7,  # J/L
        "natural_gas": 3.6e7,  # J/L
        "E85": 2.4e7,  # J/L
        "E100": 2.68e7,  # J/L
    }

    def __init__(self, fuel_type, lhv=None):
        self._fuel_type = fuel_type
        if fuel_type in Fuel._fuels_lhv:
            self._pci = Fuel._fuels_lhv[fuel_type]
        else:
            if lhv:
                self._lhv = lhv
            else:
                raise ValueError("You must provide the LHV for this fuel type")

    @property
    def fuel_type(self):
        """
        Fuel type.
        """
        return self._fuel_type

    @property
    def lhv(self):
        """
        Lower Heating Volume of the fuel in J/L.
        """
        return self._lhv
