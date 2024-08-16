import warnings


class Battery:
    """Class representing the battery of an electric vehicle"""

    def __init__(
        self,
        initial_capacity_ah: float,
        max_cycles: int,
        initial_soc_percent: float,
        voltage_v: float,
        min_health_percentage: float,
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
        min_health_percentage : float
            The minimum allowed battery health as a percentage.
        """
        self._initial_capacity_ah = initial_capacity_ah
        self.current_capacity_ah = initial_capacity_ah
        self._max_cycles = max_cycles
        self._completed_cycles = 0
        self.state_of_charge_percent = initial_soc_percent
        self._voltage_v = voltage_v
        self.min_health_percentage = min_health_percentage

    @property
    def degradation_rate(self) -> float:
        """
        Calculate the fixed degradation rate per cycle.
        """
        initial_health_percentage = 100
        allowed_health_loss = initial_health_percentage - self.min_health_percentage

        # Divide by the maximum number of cycles to get the fixed degradation rate
        # Then divide by 100 to convert percentage to a fraction
        return (allowed_health_loss / self._max_cycles) / 100

    # @property
    # def dynamic_degradation_rate(self) -> float:
    #     """
    #     Calculate the dynamic degradation rate per cycle based on current battery state.
    #     """
    #     if self._completed_cycles >= self._max_cycles:
    #         warnings.warn(
    #             "All cycles have been completed. Replace battery immediately.",
    #             UserWarning,
    #         )
    #         return 0

    #     current_health_percentage = (
    #         self.current_capacity_ah / self._initial_capacity_ah
    #     ) * 100

    #     allowed_health_loss = current_health_percentage - self.min_health_percentage
    #     remaining_cycles = self._max_cycles - self._completed_cycles

    #     if remaining_cycles <= 0:
    #         warnings.warn(
    #             "All cycles have been completed. Replace battery immediately.",
    #             UserWarning,
    #         )
    #         return 0

    #     # Calculate the dynamic degradation rate as a fraction
    #     # Divide allowed health loss by remaining cycles and then by 100 to convert percentage to a fraction
    #     return (allowed_health_loss / remaining_cycles) / 100

    def charge(self, charge_amount_ah: float) -> None:
        """
        Charge the battery by a certain amount.

        Parameters
        ----------
        charge_amount_ah : float
            The amount of charge to add to the battery in Ampere-hours.
        """

        # Get current state of charge in Ampere-hours
        soc_in_ah = self.current_capacity_ah * (self.state_of_charge_percent / 100)
        # Add the charge amount to the current state of charge
        updated_soc_in_ah = soc_in_ah + charge_amount_ah
        # Ensure the state of charge does not exceed the battery's maximum capacity
        soc_in_ah = min(updated_soc_in_ah, self.current_capacity_ah)
        # Update the state of charge percentage based on the new Ampere-hours value
        self.state_of_charge_percent = (soc_in_ah / self.current_capacity_ah) * 100

    def discharge(self, discharge_amount_ah: float) -> None:
        """
        Discharge the battery by a certain amount.

        Parameters
        ----------
        discharge_amount_ah : float
            The amount of charge to remove from the battery in Ampere-hours.
        """

        # Get current state of charge in Ampere-hours
        soc_in_ah = self.current_capacity_ah * (self.state_of_charge_percent / 100)
        # Subtract the discharge amount from the current state of charge
        updated_soc_in_ah = soc_in_ah - discharge_amount_ah

        if updated_soc_in_ah < 0:
            print("Battery depleted!")

        # Calculate the updated state of charge percentage
        updated_soc_percent = (updated_soc_in_ah / self.current_capacity_ah) * 100

        # Update the number of completed cycles based on the change in state of charge
        self._increase_completed_cycles(
            self.state_of_charge_percent, updated_soc_percent
        )
        # Update the current capacity of the battery based on degradation
        self._update_current_capacity()

        # Update the state of charge percentage
        self.state_of_charge_percent = updated_soc_percent

    def _increase_completed_cycles(
        self, initial_soc_percent: float, final_soc_percent: float
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

        # Calculate the amount of SOC change as a fraction of 100%
        cycle_increment = (initial_soc_percent - final_soc_percent) / 100
        # Increment the count of completed cycles by the calculated amount
        self._completed_cycles += cycle_increment

    def _update_current_capacity(self):
        """
        Update the current capacity of the battery based on degradation.
        """

        # Calculate the total health loss based on the number of completed cycles
        health_loss = self._completed_cycles * self.degradation_rate

        # calculate the health state substracting the loss to the total
        health_state = 1 - health_loss

        # update current capacity
        self.current_capacity_ah = self._initial_capacity_ah * health_state
