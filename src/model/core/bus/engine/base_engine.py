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


class BaseEngine:
    """
    La clase BaseEngine representa un motor base con atributos y métodos comunes.
    """

    def __init__(self, max_power, efficiency):
        """
        Inicializa una instancia de la clase BaseEngine.

        Args:
            max_power (float): La potencia máxima del motor en kilovatios (kW).
            efficiency (float): La eficiencia del motor en un rango de [0, 1].
        """
        self._max_power = max_power * 1000  # se pasa a Watts
        self.efficiency = efficiency  # en rango [0, 1]

    @property
    def max_power(self):
        """
        Obtiene la potencia máxima del motor en Watts.

        Returns:
            float: La potencia máxima del motor.
        """
        return self._max_power

    @max_power.setter
    def max_power(self, value):
        """
        Establece la potencia máxima del motor.

        Args:
            value (float): El valor de la potencia máxima en Watts.

        Notes:
            La potencia máxima debe ser un valor positivo.
        """
        if value > 0:
            self._max_power = value

    @property
    def efficiency(self):
        """
        Obtiene la eficiencia del motor.

        Returns:
            float: La eficiencia del motor en el rango [0, 1].
        """
        return self._efficiency

    @efficiency.setter
    def efficiency(self, value):
        """
        Establece la eficiencia del motor.

        Args:
            value (float): El valor de la eficiencia en el rango (0, 1].

        Raises:
            ValueError: Si la eficiencia no está en el rango (0, 1].
        """
        if 0 < value <= 1:
            self._efficiency = value
        else:
            raise ValueError("La eficiencia debe estar en el rango (0, 1]")

    def _adjust_power(self, power):
        """
        Ajusta la potencia en función de la potencia máxima y la eficiencia.

        Args:
            power (float): La potencia deseada en Watts.

        Returns:
            float: La potencia ajustada basada en la eficiencia y la potencia máxima.
        """
        if power <= self._max_power:
            return power * self._efficiency
        else:
            return self._max_power * self._efficiency

    def __str__(self):
        """
        Devuelve una representación en cadena del motor, incluyendo su tipo,
        potencia máxima y eficiencia.

        Returns:
            str: Una cadena con la información del motor.
        """
        return (
            f"Engine Type: {self.type}\n"
            f"Max Power: {self.max_power} W\n"
            f"Efficiency: {self.efficiency * 100} %"
        )
