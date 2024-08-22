class Battery:
    """Class representing the battery of an electric vehicle"""

    def __init__(
        self,
        initial_capacity_ah: float,
        voltage_v: float,
        max_cycles: int,
        initial_soc_percent: float,
        min_state_of_health: float,
    ):
        """
        Initialize a Battery instance.

        Parameters
        ----------
        initial_capacity_ah : float
            The initial capacity of the battery in Ampere-hours.
        max_cycles : int
            The maximum number of charge-discharge cycles the battery can endure.
        initial_soc_percent : float
            The initial State of Charge as a percentage.
        voltage_v : float
            The voltage of the battery in volts.
        min_state_of_health : float
            The minimum allowed battery health as a percentage.
        """
        self._initial_capacity_ah = initial_capacity_ah
        self.current_capacity_ah = initial_capacity_ah
        self._max_cycles = max_cycles
        self._completed_cycles = 0
        self.state_of_charge_percent = initial_soc_percent
        self.voltage_v = voltage_v
        self.min_state_of_health = min_state_of_health
        self._degradation_in_section = 0.0

    @property
    def degradation_rate(self) -> float:
        """Calculate the fixed degradation rate per cycle."""
        initial_state_of_health = 100
        allowed_health_loss = initial_state_of_health - self.min_state_of_health

        # Divide by the maximum number of cycles to get the fixed degradation rate
        # Then divide by 100 to convert percentage to a fraction
        return (allowed_health_loss / self._max_cycles) / 100

    @property
    def state_of_health(self):
        """Returns the current health state of the battery"""
        # Calculate the total health loss based on the number of completed cycles
        health_loss = self._completed_cycles * self.degradation_rate

        # calculate the health state substracting the loss to the total
        return 1 - health_loss

    @property
    def degradation_in_section(self) -> float:
        """Returns the percentage of degradation triggered in the current section."""
        return self._degradation_in_section

    def instant_degradation(self, time: float) -> float:
        """
        Computes the INSTANT degradation of this section.
        Receives the duration time of the section.
        """
        return self.degradation_in_section / time

    def update_soc_and_degradation(
        self, ah_transferred: float, time_seconds: float
    ) -> None:
        """
        Update the state of charge of the battery by a certain amount and apply its corresponding degradation.

        Parameters
        ----------
        ah_transferred : float
            The amount of input or output charge in Ampere-hours.
        time : float
            The duration time of the section in seconds
        """

        updated_soc_percent = self._compute_new_soc(ah_transferred)

        # Get applied electric current (Amperes)
        electric_current = self._calculate_current(ah_transferred, time_seconds)
        self._apply_degradation(updated_soc_percent, electric_current)

        # Finally, update the SoC percentage
        self.state_of_charge_percent = updated_soc_percent

    def _compute_new_soc(self, ah_transferred: float) -> float:
        """
        Updates the state of charge by a given amount in Ampere-hours.
        It ensures that the SOC does not exceed the battery's capacity or
        drop below zero.
        """

        # Get current state of charge in Ampere-hours
        current_soc_ah = self._get_soc_in_ah()
        updated_soc_in_ah = max(
            0, min(current_soc_ah - ah_transferred, self.current_capacity_ah)
        )
        # Calculate the updated State of Charge percentage
        updated_soc_percent = (updated_soc_in_ah / self.current_capacity_ah) * 100
        self._check_drained_battery(updated_soc_percent)
        return updated_soc_percent

    def _get_soc_in_ah(self) -> float:
        """Get the current state of charge in Ampere-hours."""
        return self.current_capacity_ah * (self.state_of_charge_percent / 100)

    def _check_drained_battery(self, soc_percent: float) -> None:
        if soc_percent == 0:
            print("DRAINED_BATTERY!!")

    def _calculate_current(self, ah_transferred: float, time_seconds: float) -> float:
        """
        Calculate the electric current in Amperes.

        Parameters
        ----------
        ah_transferred : float
            The charge amount in Ampere-hours.
        time_seconds : float
            The time duration in seconds.
        """
        return ah_transferred / (time_seconds / 3600)

    def _apply_degradation(
        self, updated_soc_percent: float, electric_current: float
    ) -> None:
        initial_soc_percent = self.state_of_charge_percent

        # Calculate degradation factors
        soc_factor = self._soc_degradation_factor(updated_soc_percent, electric_current)
        electric_current_factor = self._electric_current_degradation_factor(
            electric_current
        )

        # Add a factor to include information about the SoC and electric current
        adjusted_degradation_factor = soc_factor * electric_current_factor

        # Update the number of completed cycles based on the change in state of charge
        self._increase_completed_cycles(
            initial_soc_percent, updated_soc_percent, adjusted_degradation_factor
        )

        # Update the current capacity of the battery based on degradation
        self.current_capacity_ah = self._initial_capacity_ah * self.state_of_health

    def _soc_degradation_factor(
        self, soc_percent: float, electric_current: float
    ) -> float:
        """Calculate a degradation factor based on the state of charge."""

        if self._is_charging(electric_current):
            return self._calculate_charging_degradation(soc_percent)
        else:
            return self._calculate_discharging_degradation(soc_percent)

    def _is_charging(self, electric_current: float) -> bool:
        return electric_current < 0

    def _calculate_charging_degradation(self, soc_percent: float) -> float:
        """Calculate degradation factor during charging."""

        # NOTE: adjust with numerical data
        m = 0.02

        if soc_percent < 80:
            return 1.005  # Constant degradation before 80% charge
        else:
            return 1.005 + m * (soc_percent - 80)  # Linear increase after 80%

    def _calculate_discharging_degradation(self, soc_percent: float) -> float:
        """Calculate degradation factor during discharging."""

        # NOTE: adjust with numerical data
        m = 0.02

        if soc_percent > 20:
            return 1.05  # Constant degradation above 20% charge
        else:
            return 1.05 + m * (20 - soc_percent)  # Linear increase below 20%

    def _electric_current_degradation_factor(self, electric_current: float) -> float:
        """Calculate a degradation factor based on the electric current."""

        # NOTE: adjust with numerical data
        m = 0.0002

        # Determine if the battery is charging or discharging
        if self._is_charging(electric_current):
            # Greater degradation for higher positive currents during charging
            return 1 + m * electric_current
        else:
            # Greater degradation for more negative currents during discharging
            return 1 + m * abs(electric_current)

    # TODO: Ajustar este metodo porque estaba hecho pensando especificamente para
    #       incremento de ciclos cuando se descargaba la bateria. Pensar/preguntar_a_Luciano
    #       que hacer sino para marcar la degradación de la batería
    def _increase_completed_cycles(
        self,
        initial_soc_percent: float,
        final_soc_percent: float,
        factor: float,
    ) -> None:
        """
        Increment the count of completed cycles based on SOC change.

        Parameters
        ----------
        initial_soc_percent : float
            The initial state of charge as a percentage.
        final_soc_percent : float
            The final state of charge as a percentage.
        """

        # Calculate the amount of SoC change as a fraction of 100%
        cycle_increment = abs(initial_soc_percent - final_soc_percent) / 100
        # Increment the count of completed cycles by the calculated amount
        self._completed_cycles += cycle_increment * factor

        # Calculate degradation for this section
        self._degradation_in_section = cycle_increment / self._max_cycles
