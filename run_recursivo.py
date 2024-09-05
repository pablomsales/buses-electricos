    def run(self, n_iters: int = 1):
        """
        Run the model for a specified number of iterations.

        Args:
            n_iters (int): The number of iterations to run the model for.
        """
        self.run_aux(n_iters=n_iters)

    def run_aux(self, n_iters: int = 1, __consumption=0.0, __emissions=0.0, __battery_degradation=0.0):
        """
        Run the model for a specified number of iterations.

        Args:
            n_iters (int): The number of iterations to run the model for.
            __consumption (float): The accumulated consumption value.
            __emissions (float): The accumulated emissions value.
            __battery_degradation (float): The accumulated battery degradation value.
        """
        # Condición de parada de la recursividad
        if n_iters <= 0:
            # Imprimir resultados finales después de todas las iteraciones
            print(f"Consumption: {__consumption}")
            print(f"Emissions: {__emissions}")
            print(f"Battery degradation: {__battery_degradation}")
            return

        # Obtener el estado de carga de la batería (SOC)
        soc = self.soc()
        print(f"SOC: {soc}")

        # Si el SOC es inferior al 20%, cargar la batería y ajustar los cálculos
        if soc < 20.0:
            power_of_charging_point = self._get_param_by_charging_point_id(
                f"{self.charging_point_id}", "power_watts"
            )

            # Cargar la batería usando el punto de carga
            self.bus.engine.battery.charge_in_charging_point(power=power_of_charging_point)

            # Obtener la distancia al punto de carga y la longitud de la ruta
            distance_of_charging_point = self._get_param_by_charging_point_id(
                f"{self.charging_point_id}", "distance_km"
            )
            route_length_km = self.route.length_km

            # Calcular el factor para ajustar el consumo y las emisiones
            factor = (route_length_km + distance_of_charging_point) / route_length_km

            # Calcular los valores acumulados de consumo, emisiones y degradación de la batería
            new_consumption, new_emissions, new_battery_degradation = (
                self._cumulative_consumption_and_emissions()
            )

            # Ajustar los valores usando el factor calculado
            new_consumption, new_emissions, new_battery_degradation = (
                x * factor for x in (new_consumption, new_emissions, new_battery_degradation)
            )
        else:
            # Si no se necesita cargar, simplemente calcular los valores acumulados
            new_consumption, new_emissions, new_battery_degradation = (
                self._cumulative_consumption_and_emissions()
            )

        # Acumular los resultados de la iteración actual
        __consumption += new_consumption
        __emissions += new_emissions
        __battery_degradation += new_battery_degradation

        # Llamada recursiva disminuyendo n_iters
        self.run_aux(n_iters - 1, __consumption, __emissions, __battery_degradation)