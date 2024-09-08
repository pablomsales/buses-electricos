import json
import os

import folium
import matplotlib.pyplot as plt
import pandas as pd
from config import PROJECT_ROOT
from core.route.section.real_section import RealSection
from core.route.section.simulated_section import SimulatedSection


class Route:
    """
    Clase para representar una ruta con múltiples secciones.
    """

    def __init__(self, data: pd.DataFrame, bus, emissions, simulation: bool):
        """
        Inicializa la ruta con los datos proporcionados, el autobús, las emisiones y el modo.

        Args:
            data (pd.DataFrame): DataFrame que contiene la información de la ruta.
            bus: Instancia de la clase Bus.
            emissions: Instancia de la clase Emissions.
            simulation (bool): Indica si la ruta está en modo de simulación o no.
        """
        self._simulation = simulation
        self.bus = bus
        self.emissions = emissions
        self.sections = self._create_sections(data)
        self.length_km = 10.61
        self.duration_time = self._route_duration_time()
        self.charging_points = self._load_charging_points(
            os.path.join(
                PROJECT_ROOT, "data", "optimization_data", "charging_points.json"
            )
        )

    def _create_sections(self, df: pd.DataFrame) -> list:
        """
        Crea las secciones de la ruta basándose en el modo seleccionado (simulación o real).

        Args:
            df (pd.DataFrame): DataFrame que contiene la información de la ruta.

        Returns:
            list: Una lista de secciones creadas para la ruta.
        """
        if self._simulation:
            return self._process_simulated_sections(df)
        else:
            return self._process_real_sections(df)

    def _process_real_sections(self, df: pd.DataFrame) -> list:
        """
        Procesa las secciones cuando se trabaja en modo real.
        """
        sections = []
        for i in range(df.shape[0] - 1):
            start_section = df.iloc[i, :]
            end_section = df.iloc[i + 1, :]

            start_time = start_section["time"]
            end_time = end_section["time"]
            timestamps = (start_time, end_time)

            start_speed = start_section["speed"]
            end_speed = end_section["speed"]
            speeds = (start_speed, end_speed)

            start_coord = (
                float(start_section["latitude"]),
                float(start_section["longitude"]),
                float(start_section["altitude"]),
            )
            end_coord = (
                float(end_section["latitude"]),
                float(end_section["longitude"]),
                float(end_section["altitude"]),
            )
            coordinates = (start_coord, end_coord)

            section = RealSection(
                coordinates, speeds, timestamps, self.bus, self.emissions
            )
            sections.append(section)
        return sections

    def _process_simulated_sections(self, df: pd.DataFrame) -> list:
        """
        Procesa las secciones cuando se trabaja en modo de simulación.

        Args:
            df (pd.DataFrame): DataFrame que contiene la información de la ruta.

        Returns:
            list: Una lista de secciones simuladas creadas para la ruta.
        """
        # Inicializa la lista de secciones
        secciones = []
        next_initial_speed = 0
        cumulative_time = 0

        # Crea una instancia de SimulatedSection para cada segmento
        for i in range(df.shape[0] - 1):

            start_section = df.iloc[i, :]
            end_section = df.iloc[i + 1, :]

            start_coord = (
                float(start_section["latitude"]),
                float(start_section["longitude"]),
                float(start_section["altitude"]),
            )
            end_coord = (
                float(end_section["latitude"]),
                float(end_section["longitude"]),
                float(end_section["altitude"]),
            )
            coordinates = (start_coord, end_coord)

            limit = int(end_section["speed_limit"])

            # Establece el tiempo de inicio para la sección
            start_time = cumulative_time

            # Asigna la velocidad inicial para la primera sección
            initial_speed = next_initial_speed

            # Crea una instancia de SimulatedSection
            seccion = SimulatedSection(
                coordinates, limit, initial_speed, start_time, self.bus, self.emissions
            )

            # Actualiza la velocidad inicial para la siguiente sección
            next_initial_speed = seccion.end_speed

            # Velocidad inicial real para la siguiente sección
            actual_initial_speed = seccion.start_speed

            # Actualiza la velocidad final para la sección actual
            if secciones:
                secciones[-1].end_speed = actual_initial_speed

            # Actualiza el tiempo acumulado
            cumulative_time = seccion.end_time

            # Añade la sección a la lista
            secciones.append(seccion)

        # Consolida los resultados
        velocities = []
        start_times = []
        end_times = []

        for seccion in secciones:
            velocities.extend(seccion.velocities)
            start_times.append(seccion.start_time)
            end_times.append(seccion.end_time)

        # Devuelve los resultados consolidados junto con los tiempos de inicio y fin de las secciones
        return secciones

    def _route_duration_time(self):
        """
        Calcula la duración total de la ruta en segundos.
        """
        total_duration = 0
        for section in self.sections:
            total_duration += section.end_time - section.start_time
        return total_duration

    def _load_charging_points(self, file_path: str) -> dict:
        """
        Carga los puntos de carga desde un archivo JSON.

        Args:
            file_path (str): Ruta del archivo JSON con los puntos de carga.

        Returns:
            dict: Diccionario con los puntos de carga.
        """
        # Abrir y cargar el archivo JSON
        with open(file_path, "r") as archivo:
            json_data = json.load(archivo)

        # Leer la lista de puntos de carga desde el JSON
        charging_points = json_data.get("charging_points", [])

        # Crear un diccionario para almacenar los resultados
        puntos = {}

        # Iterar sobre cada punto de carga y extraer los datos requeridos
        for point in charging_points:
            # Extraer los valores requeridos
            id_ = point.get("id")
            power_watts = point.get("power_watts")
            distance_km = point.get("distance_km")
            time_min = point.get("time_min")

            # Añadir una entrada al diccionario con la ID como clave
            # y un diccionario con las claves power, distance y time como valor
            puntos[id_] = {
                "power_watts": power_watts,
                "distance_km": distance_km,
                "time_min": time_min,
            }

        return puntos

    @property
    def lenght_km(self):
        """
        Devuelve la longitud de la ruta en kilómetros.
        """
        return self.length_km

    def plot_altitude_profile(self, output_dir: str):
        """
        Traza el perfil de altitud de la ruta en función de la distancia.
        Guarda los gráficos en el directorio de salida.

        Args
        --------
        output_dir: str
            El directorio de salida
        """
        # Listas para almacenar las distancias y altitudes
        distances = []
        altitudes = []
        markers_distance = []
        markers_altitude = []

        # Variable para rastrear la distancia acumulada
        accumulated_distance = 0

        # Procesar cada sección
        for section in self.sections:
            start_altitude = section.start[2]
            end_altitude = section.end[2]

            # Añadir las distancias y altitudes de inicio y fin a las listas
            distances.append(accumulated_distance)
            altitudes.append(start_altitude)
            distances.append(accumulated_distance + section.length)
            altitudes.append(end_altitude)

            # Añadir las distancias y altitudes de inicio y fin a las listas de marcadores
            markers_distance.append(accumulated_distance)
            markers_altitude.append(start_altitude)
            markers_distance.append(accumulated_distance + section.length)
            markers_altitude.append(end_altitude)

            # Actualizar la distancia acumulada
            accumulated_distance += section.length

        # Crear el gráfico
        plt.figure(figsize=(10, 5))
        plt.plot(distances, altitudes, label="Recorrido")  # Añadir el gráfico de líneas
        plt.scatter(
            markers_distance, markers_altitude, color="red", marker="|", label="Sección"
        )  # Añadir los marcadores

        # Añadir etiquetas y título
        plt.xlabel("Distancia recorrida (m)")
        plt.ylabel("Altitud (m)")
        plt.title("Perfil de altitud en función de la distancia recorrida")
        plt.legend()

        # Mostrar el gráfico
        plt.grid(True)
        plt.savefig(os.path.join(output_dir, "altitude_profile.png"))

    def plot_speed_profile(self, output_dir: str):
        """
        Traza el perfil de velocidad de la ruta en función de la distancia.
        Guarda los gráficos en el directorio de salida.

        Args
        --------
        output_dir: str
            El directorio de salida
        """

        # Listas para almacenar las distancias y velocidades
        distances = []
        speeds = []
        markers_distance = []
        markers_speed = []

        # Variable para rastrear la distancia acumulada
        accumulated_distance = 0

        # Procesar cada sección
        for section in self.sections:

            start_speed = section.start_speed
            end_speed = section.end_speed

            # Añadir las distancias y velocidades de inicio y fin a las listas
            distances.append(accumulated_distance)
            speeds.append(start_speed)
            distances.append(accumulated_distance + section.length)
            speeds.append(end_speed)

            # Añadir las distancias y velocidades de inicio y fin a las listas de marcadores
            markers_distance.append(accumulated_distance)
            markers_speed.append(start_speed)
            markers_distance.append(accumulated_distance + section.length)
            markers_speed.append(end_speed)

            # Actualizar la distancia acumulada
            accumulated_distance += section.length

        # Crear el gráfico
        plt.figure(figsize=(10, 5))
        plt.plot(distances, speeds, label="Recorrido")  # Añadir el gráfico de líneas
        plt.scatter(
            markers_distance, markers_speed, color="red", marker="|", label="Sección"
        )  # Añadir los marcadores

        # Añadir etiquetas y título
        plt.xlabel("Distancia recorrida (m)")
        plt.ylabel("Velocidad (m/s)")
        plt.title("Perfil de velocidad en función de la distancia recorrida")
        plt.legend()

        # Mostrar el gráfico
        plt.grid(True)
        plt.savefig(os.path.join(output_dir, "speed_profile.png"))

    def plot_acceleration_profile(self, output_dir: str):
        """
        Traza el perfil de aceleración de la ruta en función de la distancia.
        Guarda los gráficos en el directorio de salida.

        Args
        --------
        output_dir: str
            El directorio de salida
        """
        # Listas para almacenar las distancias y aceleraciones
        distances = []
        accelerations = []
        markers_distance = []
        markers_acceleration = []

        # Variable para rastrear la distancia acumulada
        accumulated_distance = 0

        # Procesar cada sección
        for section in self.sections:

            # Suponiendo que _acceleration es un valor constante para cada sección
            acceleration = section._acceleration

            # Añadir las distancias y aceleraciones de inicio y fin a las listas
            distances.append(accumulated_distance)
            accelerations.append(acceleration)
            distances.append(accumulated_distance + section.length)
            accelerations.append(acceleration)

            # Añadir las distancias y aceleraciones de inicio y fin a las listas de marcadores
            markers_distance.append(accumulated_distance)
            markers_acceleration.append(acceleration)
            markers_distance.append(accumulated_distance + section.length)
            markers_acceleration.append(acceleration)

            # Actualizar la distancia acumulada
            accumulated_distance += section.length

        # Crear el gráfico
        plt.figure(figsize=(10, 5))
        plt.plot(
            distances, accelerations, label="Recorrido"
        )  # Añadir el gráfico de líneas
        plt.scatter(
            markers_distance,
            markers_acceleration,
            color="red",
            marker="|",
            label="Sección",
        )  # Añadir los marcadores

        # Añadir etiquetas y título
        plt.xlabel("Distancia recorrida (m)")
        plt.ylabel("Aceleración (m/s²)")
        plt.title("Perfil de aceleración en función de la distancia recorrida")
        plt.legend()

        plt.grid(True)
        plt.savefig(os.path.join(output_dir, "acceleration_profile.png"))

    def plot_combined_profiles(self, output_dir: str):
        """
        Combina los perfiles de altitud, velocidad y aceleración en un solo gráfico.
        """
        # Listas para almacenar los datos
        distances = []
        altitudes = []
        speeds = []
        accelerations = []
        markers_distance = []
        markers_altitude = []
        markers_acceleration = []

        # Variable para rastrear la distancia acumulada
        accumulated_distance = 0

        # Procesar cada sección
        for section in self.sections:
            # Altitud
            start_altitude = section.start[2]
            end_altitude = section.end[2]
            distances.extend(
                [accumulated_distance, accumulated_distance + section.length]
            )
            altitudes.extend([start_altitude, end_altitude])
            markers_distance.extend(
                [accumulated_distance, accumulated_distance + section.length]
            )
            markers_altitude.extend([start_altitude, end_altitude])

            # Velocidad
            start_speed = section.start_speed
            end_speed = section.end_speed
            speeds.extend([start_speed, end_speed])

            # Aceleración
            acceleration = section._acceleration
            accelerations.extend([acceleration, acceleration])
            markers_acceleration.extend([acceleration, acceleration])

            # Actualizar la distancia acumulada
            accumulated_distance += section.length

        # Crear la figura y los ejes para los subgráficos
        _, axs = plt.subplots(3, 1, figsize=(10, 15), sharex=True)

        # Graficar el perfil de altitud
        axs[0].plot(distances, altitudes, label="Recorrido")
        axs[0].scatter(
            markers_distance, markers_altitude, color="red", marker="|", label="Sección"
        )
        axs[0].set_ylabel("Altitud (m)")
        axs[0].set_title("Perfil de altitud en función de la distancia recorrida")
        axs[0].legend()
        axs[0].grid(True)

        # Graficar el perfil de velocidad
        axs[1].plot(distances, speeds, label="Recorrido")
        axs[1].scatter(
            markers_distance, speeds, color="red", marker="|", label="Sección"
        )
        axs[1].set_ylabel("Velocidad (m/s)")
        axs[1].set_title("Perfil de velocidad en función de la distancia recorrida")
        axs[1].legend()
        axs[1].grid(True)

        # Graficar el perfil de aceleración
        axs[2].plot(distances, accelerations, label="Recorrido")
        axs[2].scatter(
            markers_distance,
            markers_acceleration,
            color="red",
            marker="|",
            label="Sección",
        )
        axs[2].set_xlabel("Distancia recorrida (m)")
        axs[2].set_ylabel("Aceleración (m/s²)")
        axs[2].set_title("Perfil de aceleración en función de la distancia recorrida")
        axs[2].legend()
        axs[2].grid(True)

        # Guardar el gráfico
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "combined_profiles.png"))

    def plot_map(self, output_dir):
        """
        Traza la ruta en un mapa interactivo utilizando folium.
        """
        # Crear un mapa de folium centrado en la primera coordenada
        if not self.sections:
            raise ValueError("No hay secciones disponibles para trazar en el mapa.")

        start_coords = self.sections[0].start
        mapa = folium.Map(location=[start_coords[0], start_coords[1]], zoom_start=14)

        # Añadir líneas al mapa
        for section in self.sections:
            start_coords = section.start
            end_coords = section.end
            folium.PolyLine(
                locations=[
                    [start_coords[0], start_coords[1]],
                    [end_coords[0], end_coords[1]],
                ],
                color="blue",
                weight=2.5,
                opacity=1,
            ).add_to(mapa)

        # Guardar el mapa en un archivo HTML
        mapa.save(os.path.join(output_dir, "2D_map.html"))
