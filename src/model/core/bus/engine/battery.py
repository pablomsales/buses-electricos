"""
Proyecto: Optimización de Rutas y Análisis de Sostenibilidad en Autobuses Eléctricos Urbanos

Autores:

- Chakhoyan Grigoryan, Razmik
  Correo: chakhoyanrazmik@gmail.com
  LinkedIn: https://www.linkedin.com/in/chakhoyanrazmik

- Menéndez Sales, Pablo
  Correo: pablomenendezsales@gmail.com
  LinkedIn: https://www.linkedin.com/in/pablo-m-sales

Fecha de creación: 12/07/2024
Última modificación: 09/09/2024
"""


from time import time


class Battery:
    """
    Clase que representa la batería de un vehículo eléctrico, con funcionalidades
    para gestionar su capacidad, ciclos de carga y degradación.

    Attributes
    ----------
    voltage_v : float
        Voltaje de la batería en voltios.
    initial_capacity_kWh : float
        Capacidad inicial de la batería en kWh.
    _initial_capacity_ah : float
        Capacidad inicial de la batería en amperios-hora (Ah), calculada a partir de la capacidad en kWh.
    current_capacity_ah : float
        Capacidad actual de la batería en amperios-hora (Ah).
    _max_cycles : int
        Número máximo de ciclos de carga-descarga permitidos para la batería.
    _completed_cycles : int
        Número de ciclos de carga-descarga completados.
    state_of_charge_percent : float
        Estado actual de carga de la batería como porcentaje.
    min_state_of_health : float
        Salud mínima permitida de la batería como porcentaje.
    _degradation_in_section : float
        Degradación acumulada de la batería en la sección actual.
    min_battery_charge : float
        Carga mínima de la batería en porcentaje.
    timer_start : float or None
        Momento en el que la batería cae por debajo del nivel mínimo de carga.
    total_time_below_min_soc : float
        Tiempo total (en segundos) que la batería ha pasado por debajo de la carga mínima permitida.
    """

    def __init__(
        self,
        initial_capacity_kWh: float,
        voltage_v: float,
        max_cycles: int,
        initial_soc_percent: float,
        min_state_of_health: float,
        min_battery_charge: float,
    ):
        """
        Parameters
        ----------
        initial_capacity_kWh : float
            Capacidad inicial de la batería en kWh.
        voltage_v : float
            Voltaje de la batería en voltios.
        max_cycles : int
            Número máximo de ciclos de carga-descarga que la batería puede soportar.
        initial_soc_percent : float
            Estado inicial de carga (State of Charge, SoC) como porcentaje.
        min_state_of_health : float
            Salud mínima de la batería permitida como porcentaje.
        min_battery_charge : float
            Carga mínima de la batería en porcentaje, antes de que sea necesario recargarla.
        """

        self.voltage_v = voltage_v
        self.initial_capacity_kWh = initial_capacity_kWh
        self._initial_capacity_ah = self._convert_kWh_to_Ah(initial_capacity_kWh)
        self.current_capacity_ah = self._convert_kWh_to_Ah(initial_capacity_kWh)
        self._max_cycles = max_cycles
        self._completed_cycles = 0
        self.state_of_charge_percent = initial_soc_percent
        self.min_state_of_health = min_state_of_health
        self._degradation_in_section = 0.0
        self.min_battery_charge = min_battery_charge
        self.timer_start = None
        self.total_time_below_min_soc = 0

    def _convert_kWh_to_Ah(self, kWh: float) -> float:
        """
        Convert energy in kilowatt-hours to ampere-hours based on the battery voltage.

        :param kWh: Energy in kilowatt-hours
        :return: Capacity in ampere-hours
        """
        if self.voltage_v <= 0:
            raise ValueError("Voltage must be greater than zero.")

        return (kWh * 1000) / self.voltage_v

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
        self.check_soc_under_minimum(self.state_of_charge_percent)

    def charge_in_charging_point(self, power: int, desired_soc: float) -> float:
        """
        Charge the battery in a charging point.

        Parameters
        ----------
        power : int
            The power in Watts.
        desired_soc : float
            The desired state of charge as a percentage (0-100).
        """
        # Calculate the time needed to reach the desired SoC
        time_seconds = self._calculate_time_to_charge(power, desired_soc)
        # Convert Watts to Ah
        ah_transferred = self._calculate_current(power=power) * (time_seconds / 3600)

        # Update the state of charge and apply degradation
        self.update_soc_and_degradation(-ah_transferred, time_seconds)

        return time_seconds

    def _calculate_time_to_charge(self, power: int, desired_soc: float) -> float:
        """
        Calculate the time needed to charge the battery to a desired state of charge.

        Parameters
        ----------
        power : int
            The power in Watts.
        desired_soc : float
            The desired state of charge as a percentage (0-100).

        Returns
        -------
        float
            The time needed to charge the battery in seconds.
        """
        if power <= 0:
            raise ValueError("La potencia debe ser mayor que 0.")

        # Calculate the amount of charge needed to reach the desired SoC
        desired_soc_ah = (desired_soc / 100) * self.current_capacity_ah
        charge_needed = desired_soc_ah - self._get_soc_in_ah()

        # Calculate the time needed to charge the battery
        return ((charge_needed * self.voltage_v) / power) * 3600

    def _compute_new_soc(self, ah_transferred: float) -> float:
        """
        Updates the state of charge by a given amount in Ampere-hours.
        It ensures that the SOC does not exceed the battery's capacity.
        It doesn't handle the case of negative values of SoC because
        of reasons for optimizing better the parameters of the bus.
        """

        # Get current state of charge in Ampere-hours
        current_soc_ah = self._get_soc_in_ah()
        updated_soc_in_ah = min(
            current_soc_ah - ah_transferred, self.current_capacity_ah
        )
        # Calculate the updated State of Charge percentage
        updated_soc_percent = (updated_soc_in_ah / self.current_capacity_ah) * 100
        return updated_soc_percent

    def _get_soc_in_ah(self) -> float:
        """Get the current state of charge in Ampere-hours."""
        return self.current_capacity_ah * (self.state_of_charge_percent / 100)

    def check_soc_under_minimum(self, soc_percent: float):
        """
        Verifica si el estado de carga (SoC) de la batería está por debajo del mínimo permitido y gestiona
        un cronómetro que mide el tiempo total en el que la batería ha estado por debajo de ese umbral.

        Si el SoC está por debajo del nivel mínimo y el cronómetro no está activo, lo inicia.
        Si el SoC sube por encima del nivel mínimo y el cronómetro está activo, calcula el tiempo transcurrido
        por debajo del umbral y lo acumula en `total_time_below_min_soc`.

        Parameters
        ----------
        soc_percent : float
            El porcentaje actual del estado de carga (SoC) de la batería.
        """
        if soc_percent < self.min_battery_charge:
            if self.timer_start is None:  # Si el cronómetro no ha iniciado
                self.timer_start = time()  # Inicia el cronómetro
        else:
            if self.timer_start is not None:  # Si el cronómetro está corriendo
                time_below_min = time() - self.timer_start
                self.total_time_below_min_soc += (
                    time_below_min  # Actualiza el tiempo total
                )
                self.timer_start = None  # Detén el cronómetro

    def _calculate_current(
        self,
        ah_transferred: float = None,
        time_seconds: float = None,
        power: int = None,
    ) -> float:
        """
        Calculate the electric current in Amperes based on the power, or the transferred charge and time.

        Parameters
        ----------
        ah_transferred : float
            The amount of input or output charge in Ampere-hours.
        time_seconds : float
            The duration time of the section in seconds.
        power : int
            The power in Watts.

        Returns
        -------
        float
            The electric current in Amperes.
        """
        if power:
            if power <= 0:
                raise ValueError("La potencia debe ser mayor que 0.")
            return power / self.voltage_v

        if ah_transferred and time_seconds:
            if time_seconds <= 0:
                raise ValueError("El tiempo en segundos debe ser mayor que 0.")
            return ah_transferred / (time_seconds / 3600)

        raise ValueError(
            "Debe proporcionar 'power', o ambos 'ah_transferred' y 'time_seconds' para calcular la intensidad."
        )

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
