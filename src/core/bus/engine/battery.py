class Battery:
    """Class representing the battery of an electric vehicle"""

    def __init__(
        self,
        initial_capacity_ah: float,
        voltage_v: float,
        max_cycles: int,
        initial_soc_percent: float,
        min_depth_of_discharge: float,
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
        min_depth_of_discharge : float
            The minimum allowed battery health as a percentage.
        """
        self._initial_capacity_ah = initial_capacity_ah
        self.current_capacity_ah = initial_capacity_ah
        self._max_cycles = max_cycles
        self._completed_cycles = 0
        self.state_of_charge_percent = initial_soc_percent
        self.voltage_v = voltage_v
        self.min_depth_of_discharge = min_depth_of_discharge
        self._degradation_in_section = 0.0

    @property
    def degradation_rate(self) -> float:
        """Calculate the fixed degradation rate per cycle."""
        initial_depth_of_discharge = 100
        allowed_health_loss = initial_depth_of_discharge - self.min_depth_of_discharge

        # Divide by the maximum number of cycles to get the fixed degradation rate
        # Then divide by 100 to convert percentage to a fraction
        return (allowed_health_loss / self._max_cycles) / 100

    @property
    def depth_of_discharge(self):
        """Returns the current health state of the battery"""
        # Calculate the total health loss based on the number of completed cycles
        health_loss = self._completed_cycles * self.degradation_rate

        # calculate the health state substracting the loss to the total
        return 1 - health_loss

    @property
    def degradation_in_section(self) -> float:
        """Returns the percentage of degradation triggered in the current section."""
        return self._degradation_in_section

    def charge(self, charge_amount_ah: float) -> None:
        """
        Charge the battery by a certain amount.

        Parameters
        ----------
        charge_amount_ah : float
            The amount of charge to add to the battery in Ampere-hours.
        """
        self.state_of_charge_percent = self._update_state_of_charge(charge_amount_ah)

    def discharge(self, discharge_amount_ah: float, time_seconds: float) -> None:
        """
        Discharge the battery by a certain amount.

        Parameters
        ----------
        discharge_amount_ah : float
            The amount of charge to remove from the battery in Ampere-hours.
        time : float
            The duration time of the section in seconds
        """

        # Calculate the updated state of charge percentage
        # TODO: Chequear si discharge_amount es un numero negativo, sino, hay que:
        #   - o bien pasarlo negativo de primeras
        #   - o bien pasar como parametro `-discharge_amount_ah` aqui debajo
        updated_soc_percent = self._update_state_of_charge(discharge_amount_ah)

        # Get applied electric current (Amperes)
        electric_current = self._calculate_current(discharge_amount_ah, time_seconds)
        self._apply_degradation(updated_soc_percent, electric_current)

        # Finally, update the SoC percentage
        self.state_of_charge_percent = updated_soc_percent

    def instant_degradation(self, time: float) -> float:
        """
        Computes the INSTANT degradation of this section.
        Receives the duration time of the section.
        """
        return self.degradation_in_section / time

    def _update_state_of_charge(self, amount_ah: float) -> float:
        """
        Updates the state of charge by a given amount in Ampere-hours.
        It ensures that the SOC does not exceed the battery's capacity or
        drop below zero.
        """

        # Get current state of charge in Ampere-hours
        current_soc_ah = self._get_soc_in_ah()
        updated_soc_in_ah = max(
            0, min(current_soc_ah - amount_ah, self.current_capacity_ah)
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

    def _calculate_current(self, amount_ah: float, time_seconds: float) -> float:
        """
        Calculate the electric current in Amperes.

        Parameters
        ----------
        amount_ah : float
            The charge amount in Ampere-hours.
        time_seconds : float
            The time duration in seconds.
        """
        return amount_ah / (time_seconds / 3600)

    def _apply_degradation(
        self, updated_soc_percent: float, electric_current: float
    ) -> None:
        initial_soc_percent = self.state_of_charge_percent

        # Calculate degradation factors
        soc_factor = self._soc_degradation_factor(updated_soc_percent)
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
        self.current_capacity_ah = self._initial_capacity_ah * self.depth_of_discharge

    def _soc_degradation_factor(self, soc_percent: float) -> float:
        """Calculate a degradation factor based on the state of charge."""

        # Example function: more degradation at the extremes
        # Quadratic increase away from 50%
        # TODO: esta bien esta funcion???
        return 1 + 0.5 * (max(abs(soc_percent - 50) / 50, 1))

    def _electric_current_degradation_factor(self, electric_current: float) -> float:
        """Calculate a degradation factor based on the electric current."""

        # Example function: linear increase with current
        # TODO: 0.0001 esta bien???
        return 1 + 0.0001 * electric_current  # Linear increase for simplicity

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
        cycle_increment = (initial_soc_percent - final_soc_percent) / 100
        # Increment the count of completed cycles by the calculated amount
        self._completed_cycles += cycle_increment * factor

        # Calculate degradation for this section
        self._degradation_in_section = cycle_increment / self._max_cycles
