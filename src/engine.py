from fuel import Fuel

class Engine:
    '''
    Engine class represents the engine of a vehicle. It can be either combustion or electric.
    '''
    def __init__(self, engine_type, max_power, efficiency, fuel=None):
        self._engine_type = engine_type  # "combustion" or "electric"
        self._max_power = max_power  # in Watts
        self._efficiency = efficiency  # between 0 and 1
        if engine_type != "electric":
            if fuel:
                self._fuel = fuel  # Fuel instance
            else:
                raise ValueError("Fuel parameter expected for engine_type='combustion'")

    @property
    def engine_type(self):
        '''
        Engine type object.
        '''
        return self._engine_type

    @engine_type.setter
    def engine_type(self, value):
        if value in ["combustion", "electric"]:
            self._engine_type = value
        else:
            raise ValueError("Engine type must be either 'combustion' or 'electric'")

    @property
    def fuel(self):
        '''
        Fuel object representing the fuel used by the engine.
        '''
        return self._fuel

    @fuel.setter
    def fuel(self, value):
        if isinstance(value, Fuel):
            self._fuel = value

    @property
    def max_power(self):
        '''
        Maximum power of the engine in Watts.
        '''
        return self._max_power

    @max_power.setter
    def max_power(self, value):
        if value > 0:
            self._max_power = value

    @property
    def efficiency(self):
        '''
        Efficiency of the engine in the range [0, 1].
        '''
        return self._efficiency

    @efficiency.setter
    def efficiency(self, value):
        if 0 < value <= 1:
            self._efficiency = value

    def required_power(self, desired_power):
        '''
        Computes overall needed power (Watts) considering the efficiency.
        '''
        if desired_power <= self._max_power:
            effective_power = desired_power * self._efficiency
        else:
            effective_power = self._max_power * self._efficiency

        additional_power = desired_power - effective_power
        return desired_power + additional_power

    def consumption(self, desired_power, time, kilometers=None):
        '''
        Calculate the overall energy or fuel consumption.
        '''
        total_power = self.required_power(desired_power)

        if self.engine_type == "electric":
            hours = time / 3600  # convert seconds to hours
            consumption = total_power * hours  # compute Wh

        else:
            if kilometers:
                pci = self.fuel.pci  # obtain selected fuel PCI
                energy = total_power * time  # compute amount of energy
                litres = energy / pci  # obtain the spent litres of fuel
                consumption = litres / kilometers  # finally, compute L/km
            else:
                raise ValueError("Kilometers parameter expected")

        return consumption

    def __str__(self):
        return (
            f"Engine Type: {self.type}\n"
            f"Max Power: {self.max_power} W\n"
            f"Efficiency: {self.efficiency * 100} %"
        )
