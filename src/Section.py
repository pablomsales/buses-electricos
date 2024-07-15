class Section:

    def __init__(self, coordinates, speeds, timestamps):
        self._coordinates = coordinates
        self._speeds = speeds
        self._timestamps = timestamps
        self._mass = 0
        self._motion_resistance = 0

    @property
    def start_coordinates(self):
        """
        Gets first element in coordinates tuple
        """
        return self._coordinates[0]

    @property
    def end_coordinates(self):
        """
        Gets 2nd element in coordinates tuple
        """
        return self._coordinates[1]

    @property
    def start_speed(self):
        """
        Gets speed at starting point
        """
        return self._coordinates[0]

    @property
    def end_speed(self):
        """
        Gets speed at ending point
        """
        return self._coordinates[1]

    @property
    def mass(self):
        return self._mass

    @mass.setter
    def mass(self, valor):
        if valor > 0:
            self._mass += valor
