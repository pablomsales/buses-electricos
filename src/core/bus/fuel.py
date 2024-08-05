from utils.constants import fuels_lhv


class Fuel:
    """
    Class representing a fuel type.
    """

    def __init__(self, fuel_type, lhv=None):
        self._fuel_type = fuel_type
        if fuel_type in fuels_lhv:
            self._lhv = fuels_lhv[fuel_type]
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
