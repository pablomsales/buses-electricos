import os

import folium
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from section import Section


class Route:
    """
    Class to represent a route with multiple sections.
    """

    def __init__(self, filepath, bus, emissions):
        if filepath:
            self._data = self.__load_data(filepath)
            self.bus = bus
            self.emissions = emissions
            self.sections = self.__process_sections(self._data)
        else:
            raise ValueError(
                "No file path provided. Please provide a file path to load data."
            )

    def __load_data(self, filepath: str):
        """
        Load data from a file.
        """
        if filepath.endswith(".csv"):
            data = self.__process_csv(filepath)
        elif filepath.endswith(".gpx"):
            data = self.__process_gpx(filepath)
        else:
            raise ValueError(
                "Unsupported file format. Only .csv and .gpx are supported."
            )
        return data

    def __process_csv(self, filepath):
        """
        Process the CSV file.
        """
        df = pd.read_csv(filepath)
        df = df.iloc[:, [2, 3, 4, 6, 8, 9]]
        df.columns = ["time", "latitude", "longitude", "altitude", "distance", "speed"]
        if df.iloc[0]["time"] == 0:
            first_non_zero_index = df[df["time"] != 0].index[0]
            df = df.iloc[first_non_zero_index - 1 :]
        return df

    def __process_sections(self, df: pd.DataFrame):
        """
        Process the sections of the route.
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
                start_section["latitude"],
                start_section["longitude"],
                start_section["altitude"],
            )
            end_coord = (
                end_section["latitude"],
                end_section["longitude"],
                end_section["altitude"],
            )
            coordinates = (start_coord, end_coord)

            section = Section(coordinates, speeds, timestamps, self.bus, self.emissions)
            sections.append(section)
        return sections

    def altitude_profile_plot(self):
        """
        Plots the altitude profile of the route based on distance.
        """
        # Lists to store the distances and altitudes
        distances = []
        altitudes = []
        markers_distance = []
        markers_altitude = []

        # Variable to track the accumulated distance
        accumulated_distance = 0

        # Process each section
        for section in self.sections:
            start_coords, end_coords = section._coordinates

            start_altitude = start_coords[2]
            end_altitude = end_coords[2]

            # Add the start and end distances and altitudes to the lists
            distances.append(accumulated_distance)
            altitudes.append(start_altitude)
            distances.append(accumulated_distance + section.length)
            altitudes.append(end_altitude)

            # Add the start and end distances and altitudes to the markers lists
            markers_distance.append(accumulated_distance)
            markers_altitude.append(start_altitude)
            markers_distance.append(accumulated_distance + section.length)
            markers_altitude.append(end_altitude)

            # Update the accumulated distance
            accumulated_distance += section.length

        # Crear el gráfico
        plt.figure(figsize=(10, 5))
        plt.plot(distances, altitudes, label="Recorrido")  # Add the line plot
        plt.scatter(
            markers_distance, markers_altitude, color="red", marker="|", label="Sección"
        )  # Add the markers

        # Añadir etiquetas y título
        plt.xlabel("Distancia recorrida (m)")
        plt.ylabel("Altitud (m)")
        plt.title("Perfil de altitud en función de la distancia recorrida")
        plt.legend()

        # Mostrar el gráfico
        plt.grid(True)
        self._save_plot("altitude_profile.png")

    def speed_profile_plot(self):
        """
        Plots the speed profile of the route based on distance.
        """
        # Lists to store the distances and speeds
        distances = []
        speeds = []
        markers_distance = []
        markers_speed = []

        # Variable to track the accumulated distance
        accumulated_distance = 0

        # Process each section
        for section in self.sections:

            start_speed = section._speeds[
                0
            ]  # Assuming _speeds is a tuple (start_speed, end_speed)
            end_speed = section._speeds[1]

            # Add the start and end distances and speeds to the lists
            distances.append(accumulated_distance)
            speeds.append(start_speed)
            distances.append(accumulated_distance + section.length)
            speeds.append(end_speed)

            # Add the start and end distances and speeds to the markers lists
            markers_distance.append(accumulated_distance)
            markers_speed.append(start_speed)
            markers_distance.append(accumulated_distance + section.length)
            markers_speed.append(end_speed)

            # Update the accumulated distance
            accumulated_distance += section.length

        # Create the plot
        plt.figure(figsize=(10, 5))
        plt.plot(distances, speeds, label="Recorrido")  # Add the line plot
        plt.scatter(
            markers_distance, markers_speed, color="red", marker="|", label="Sección"
        )  # Add the markers

        # Add labels and title
        plt.xlabel("Distancia recorrida (m)")
        plt.ylabel("Velocidad (m/s)")
        plt.title("Perfil de velocidad en función de la distancia recorrida")
        plt.legend()

        # Show the plot
        plt.grid(True)
        self._save_plot("speed_profile.png")

    def acceleration_profile_plot(self):
        """
        Plots the acceleration profile of the route based on distance.
        """
        # Lists to store the distances and accelerations
        distances = []
        accelerations = []
        markers_distance = []
        markers_acceleration = []

        # Variable to track the accumulated distance
        accumulated_distance = 0

        # Process each section
        for section in self.sections:

            # Assuming _acceleration is a constant value for each section
            acceleration = section._acceleration

            # Add the start and end distances and accelerations to the lists
            distances.append(accumulated_distance)
            accelerations.append(acceleration)
            distances.append(accumulated_distance + section.length)
            accelerations.append(acceleration)

            # Add the start and end distances and accelerations to the markers lists
            markers_distance.append(accumulated_distance)
            markers_acceleration.append(acceleration)
            markers_distance.append(accumulated_distance + section.length)
            markers_acceleration.append(acceleration)

            # Update the accumulated distance
            accumulated_distance += section.length

        # Create the plot
        plt.figure(figsize=(10, 5))
        plt.plot(distances, accelerations, label="Recorrido")  # Add the line plot
        plt.scatter(
            markers_distance,
            markers_acceleration,
            color="red",
            marker="|",
            label="Sección",
        )  # Add the markers

        # Add labels and title
        plt.xlabel("Distancia recorrida (m)")
        plt.ylabel("Aceleración (m/s²)")
        plt.title("Perfil de aceleración en función de la distancia recorrida")
        plt.legend()

        # Show the plot
        plt.grid(True)
        self._save_plot("acceleration_profile.png")

    def combined_profiles_plot(self):
        """
        Combines the altitude, speed, and acceleration profiles in a single plot.
        """
        # Lists to store the data
        distances = []
        altitudes = []
        speeds = []
        accelerations = []
        markers_distance = []
        markers_altitude = []
        markers_acceleration = []

        # Variable to track the accumulated distance
        accumulated_distance = 0

        # Process each section
        for section in self.sections:
            # Altitude
            start_altitude = section._coordinates[0][2]
            end_altitude = section._coordinates[1][2]
            distances.extend(
                [accumulated_distance, accumulated_distance + section.length]
            )
            altitudes.extend([start_altitude, end_altitude])
            markers_distance.extend(
                [accumulated_distance, accumulated_distance + section.length]
            )
            markers_altitude.extend([start_altitude, end_altitude])

            # Speed
            start_speed = section._speeds[0]
            end_speed = section._speeds[1]
            speeds.extend([start_speed, end_speed])

            # Acceleration
            acceleration = section._acceleration
            accelerations.extend([acceleration, acceleration])
            markers_acceleration.extend([acceleration, acceleration])

            # Update the accumulated distance
            accumulated_distance += section.length

        # Create the figure and axes for the subplots
        _, axs = plt.subplots(3, 1, figsize=(10, 15), sharex=True)

        # Plot altitude profile
        axs[0].plot(distances, altitudes, label="Recorrido")
        axs[0].scatter(
            markers_distance, markers_altitude, color="red", marker="|", label="Sección"
        )
        axs[0].set_ylabel("Altitud (m)")
        axs[0].set_title("Perfil de altitud en función de la distancia recorrida")
        axs[0].legend()
        axs[0].grid(True)

        # Plot speed profile
        axs[1].plot(distances, speeds, label="Recorrido")
        axs[1].scatter(
            markers_distance, speeds, color="red", marker="|", label="Sección"
        )
        axs[1].set_ylabel("Velocidad (m/s)")
        axs[1].set_title("Perfil de velocidad en función de la distancia recorrida")
        axs[1].legend()
        axs[1].grid(True)

        # Plot acceleration profile
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

        # Save the plot
        plt.tight_layout()
        self._save_plot("combined_profiles.png")

    def _save_plot(self, filename):
        # Obtener la ruta absoluta del directorio donde está el script actual
        this_script_dir = os.path.dirname(os.path.abspath(__file__))

        # Construir la ruta relativa al directorio de destino
        output_dir = os.path.join(this_script_dir, "..", "maps_plots")

        # Crear el directorio si no existe
        os.makedirs(output_dir, exist_ok=True)

        # Construir la ruta completa del archivo de salida
        output_path = os.path.join(output_dir, filename)

        # Guardar la imagen
        plt.savefig(output_path)

    def plot_map(self, output_file="mapa_secciones.html"):
        """
        Plots the route on an interactive map using folium.
        """
        # Create a folium map centered on the first coordinate
        if not self.sections:
            raise ValueError("No sections available to plot on the map.")

        start_coords = self.sections[0].start_coord
        mapa = folium.Map(location=[start_coords[0], start_coords[1]], zoom_start=14)

        # Add lines to the map
        for section in self.sections:
            start_coords = section.start_coord
            end_coords = section.end_coord
            folium.PolyLine(
                locations=[
                    [start_coords[0], start_coords[1]],
                    [end_coords[0], end_coords[1]],
                ],
                color="blue",
                weight=2.5,
                opacity=1,
            ).add_to(mapa)

        # Save the map to an HTML file
        mapa.save(os.path.join("maps_plots", output_file))
        print(
            f"\n---------------------------------------------------\nMap saved to {output_file}"
        )
