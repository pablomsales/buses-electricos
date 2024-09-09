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


from utils.constants import fuels_lhv

class Fuel:
    """
    Clase que representa un tipo de combustible.
    """

    def __init__(self, fuel_type, lhv=None):
        """
        Inicializa una instancia de Fuel.

        Args:
            fuel_type (str): El tipo de combustible.
            lhv (float, opcional): El Valor Calorífico Inferior (Lower Heating Value) del combustible en J/L.

        Raises:
            ValueError: Si el tipo de combustible no está en `fuels_lhv` y no se proporciona un LHV.
        """
        self._fuel_type = fuel_type
        if fuel_type in fuels_lhv:
            self._lhv = fuels_lhv[fuel_type]
        else:
            if lhv:
                self._lhv = lhv
            else:
                raise ValueError("Debe proporcionar el LHV para este tipo de combustible")

    @property
    def fuel_type(self):
        """
        Obtiene el tipo de combustible.

        Returns:
            str: Tipo de combustible.
        """
        return self._fuel_type

    @property
    def lhv(self):
        """
        Obtiene el Valor Calorífico Inferior del combustible en J/L.

        Returns:
            float: Valor Calorífico Inferior (LHV) en J/L.
        """
        return self._lhv
