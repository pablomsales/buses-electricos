from engine import Engine

class Bus:
    def __init__(self, mass, drag_coefficient, frontal_area, rolling_resistance_coefficient, engine):
        self._mass = mass
        self._drag_coefficient = drag_coefficient
        self._frontal_area = frontal_area
        self._rolling_resistance_coefficient = rolling_resistance_coefficient
        self._engine = engine

    @property
    def mass(self):
        return self._mass

    @mass.setter
    def mass(self, value):
        if value > 0:
            self._mass = value

    @property
    def drag_coefficient(self):
        return self._drag_coefficient

    @drag_coefficient.setter
    def drag_coefficient(self, value):
        if 0 < value < 1:  # typical values for drag coefficient
            self._drag_coefficient = value

    @property
    def frontal_area(self):
        return self._frontal_area

    @frontal_area.setter
    def frontal_area(self, value):
        if value > 0:
            self._frontal_area = value

    @property
    def rolling_resistance_coefficient(self):
        return self._rolling_resistance_coefficient

    @rolling_resistance_coefficient.setter
    def rolling_resistance_coefficient(self, value):
        if value > 0:
            self._rolling_resistance_coefficient = value

    @property
    def engine(self):
        return self._engine

    @engine.setter
    def engine(self, value):
        if isinstance(value, Engine):
            self._engine = value

    def __str__(self):
        return (
            f"Bus Characteristics:\n"
            f"Mass: {self.mass} kg\n"
            f"Drag Coefficient: {self.drag_coefficient}\n"
            f"Frontal Area: {self.frontal_area} m²\n"
            f"Rolling Resistance Coefficient: {self.rolling_resistance_coefficient}\n"
            f"{str(self.engine)}"
        )
