from core.section.base_section import BaseSection

max_acceleration = 1.5  # m/s^2
max_deceleration = -1.0  # m/s^2, note this is negative

class SimulatedSection(BaseSection):
    def __init__(self, coordinates, speed_limit, start_speed, start_time, bus, emissions):
        """
        Initialize a SimulatedSection with coordinates, bus, emissions, a single speed limit, 
        start speed, and start time.

        Args:
            coordinates (tuple): A tuple containing start and end coordinates.
            speed_limit (float): Speed limit (km/h) for the section.
            start_speed (float): Speed at the beginning of the section (m/s).
            start_time (float): Time at the beginning of the section (s).
            bus: Instance of the Bus class.
            emissions: Instance of the Emissions class.
        """
        self._speed_limit = speed_limit / 3.6  # Convert km/h to m/s
        self._start_speed = start_speed
        self._start_time = start_time
        self._end_speed = 0.0
        self._end_time = 0.0
        self.velocities = []          # List of average velocities
        self.start_times = []         # List of start times
        self.end_times = []           # List of end times
        
        # Call base class to initialize necessary attributes
        super().__init__(coordinates, bus, emissions)
        
        # Process the section
        self._process()

    def _process(self):
        """Calculate the speed and time for the given section considering total resistance."""
        dist = self.length  # Distance of the section
        limit = self._speed_limit
        
        # Calculate effective acceleration and deceleration based on total resistance
        effective_max_acceleration, effective_max_deceleration = self._calculate_effective_forces()
        
        # Calculate end speed based on the speed limit and start speed
        self._end_speed, decel, accel = self._calculate_end_speed(limit, dist, effective_max_acceleration, effective_max_deceleration)

        if accel is not None and decel is None:
            # Set acceleration to the calculated value
            self._acceleration = accel
        elif decel is not None and accel is None:
            # Set deceleration to the calculated value
            self._acceleration = decel
        else:
            # No change in speed
            self._acceleration = 0.0
        
        # Calculate the time required to traverse the section
        self._end_time = self._calculate_time(decel, accel, dist)
        
        # Calculate and store the average speed
        avg_speed = self._calculate_average_speed()  
        self.velocities.append(avg_speed)
        self.start_times.append(self._start_time)
        self.end_times.append(self._end_time)

    def _calculate_effective_forces(self):
        """Calculate effective acceleration and deceleration based on the total resistance."""
        total_resistance = self.total_resistance  # N
        effective_max_acceleration = max_acceleration - (total_resistance / self.bus.mass)
        effective_max_deceleration = max_deceleration + (total_resistance / self.bus.mass)
        return effective_max_acceleration, effective_max_deceleration

    def _decelerate_to_stop(self, dist, effective_max_deceleration, step_size=1.0):
        """Handles the case where the speed must be reduced to zero by reducinng the
        initial speed while the calculated deceleration is greater than the maximum deceleration allowed."""
        self._end_speed = 0
        decel = (-self._start_speed**2) / (2 * dist)
        while abs(decel) > abs(effective_max_deceleration):
            if self._start_speed - step_size >= 0:
                self._start_speed -= step_size
            decel = (-self._start_speed**2) / (2 * dist)
        return decel, None

    def _decelerate(self, limit, dist, effective_max_deceleration, step_size=1.0):
        """Handles the case where the speed must be reduced to a certain limit by reducing the
        initial speed while the calculated deceleration is greater than the maximum deceleration allowed."""
        self._end_speed = limit
        decel = (self._end_speed**2 - self._start_speed**2) / (2 * dist)
        while abs(decel) > abs(effective_max_deceleration):
            if self._end_speed - step_size >= 0:
                self._end_speed -= step_size
            if self._start_speed - step_size >= 0:
                self._start_speed -= step_size
            decel = (self._end_speed**2 - self._start_speed**2) / (2 * dist)
        return decel, None

    def _accelerate(self, limit, dist, effective_max_acceleration, step_size=1.0):
        """Handles the case where the speed must be increased to a certain limit by reducing the
        initial speed while the calculated acceleration is greater than the maximum acceleration allowed."""
        self._end_speed = limit
        accel = (self._end_speed**2 - self._start_speed**2) / (2 * dist)
        while abs(accel) > abs(effective_max_acceleration):
            if self._end_speed - step_size >= 0:
                self._end_speed -= step_size
            if self._start_speed - step_size >= 0:
                self._start_speed -= step_size
            accel = (self._end_speed**2 - self._start_speed**2) / (2 * dist)
        return None, accel

    def _calculate_end_speed(self, limit, dist, effective_max_acceleration, effective_max_deceleration):
        """Determine the end speed, and possible acceleration or deceleration."""
        if limit == 0:
            decel, accel = self._decelerate_to_stop(dist, effective_max_deceleration)
        elif limit < self._start_speed:
            decel, accel = self._decelerate(limit, dist, effective_max_deceleration)
        elif limit > self._start_speed:
            decel, accel = self._accelerate(limit, dist, effective_max_acceleration)
        else:
            self._end_speed = limit
            decel, accel = None, None

        # Return the final end speed, deceleration, and acceleration
        return self._end_speed, decel, accel

    def _calculate_time(self, decel, accel, dist):
        """Calculate the time required to traverse the section."""
        if decel is not None and decel < 0:
            time = (self._start_speed - self._end_speed) / abs(decel)  # t = (vi - vf) / |a|
        elif accel is not None and accel > 0:
            time = (self._end_speed - self._start_speed) / accel
        else:
            time = dist / max(self._start_speed, 0.1)
        
        return self._start_time + time
    
    @property
    def acceleration(self):
        return self._acceleration
    
    @acceleration.setter
    def acceleration(self, value):
        self._acceleration = value

    @property
    def start_speed(self):
        return self._start_speed
    
    @start_speed.setter
    def start_speed(self, value):
        self._start_speed = value

    @property
    def end_speed(self):
        return self._end_speed
    
    @end_speed.setter
    def end_speed(self, value):
        self._end_speed = value

    @property
    def start_time(self):
        return self._start_time
    
    @start_time.setter
    def start_time(self, value):
        self._start_time = value

    @property
    def end_time(self):
        return self._end_time
    
    @end_time.setter
    def end_time(self, value):
        self._end_time = value

    def __str__(self):
        return (
            f"Simulated Section from {self._start[0]} º, {self._start[1]} º, {round(self._start[2], 2)} m "
            f"to {self._end[0]} º, {self._end[1]} º, {round(self._end[2], 2)} m\n"
            f"Speeds: {round(self.start_speed, 2)} m/s to {round(self.end_speed, 2)} m/s\n"
            f"Time Elapsed: {round(self.duration_time, 2)} s\n"
            f"Distance: {round(self.length, 2)} m\n"
            f"Total Resistance: {round(self.total_resistance, 2)} N\n"
            f"Calculated Acceleration/Deceleration: {round(self.acceleration, 2)} m/s^2\n"
        )
