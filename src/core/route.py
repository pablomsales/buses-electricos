import os

import folium
import matplotlib.pyplot as plt
import pandas as pd

from core.section.simulated_section import SimulatedSection
from core.section.real_section import RealSection


class Route:
    """
    Class to represent a route with multiple sections.
    """

    def __init__(self, data: pd.DataFrame, bus, emissions, mode: str):
        """
        Initialize the Route with provided data, bus, emissions, and mode.

        Args:
            data (pd.DataFrame): DataFrame containing route information.
            bus: Instance of the Bus class.
            emissions: Instance of the Emissions class.
            mode (str): Mode of operation, either 'real' or 'simulation'.
        """
        self._mode = mode
        self.bus = bus
        self.emissions = emissions
        self.sections = self._create_sections(data)

    def _create_sections(self, df: pd.DataFrame) -> list:
        """
        Creates the sections of the route based on the mode.

        Args:
            df (pd.DataFrame): DataFrame containing route information.

        Returns:
            list: A list of sections created for the route.

        Raises:
            ValueError: If the mode is invalid.
        """
        if self._mode == "real":
            return self._process_real_sections(df)
        elif self._mode == "simulation":
            return self._process_simulated_sections(df)
        else:
            raise ValueError("Invalid mode. Mode should be 'real' or 'simulation'.")

    def _process_real_sections(self, df: pd.DataFrame) -> list:
        """
        Process sections when working in real mode
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
        Process sections when working in simulation mode.

        Args:
            df (pd.DataFrame): DataFrame containing route information.

        Returns:
            list: A list of simulated sections created for the route.
        """
        # Initialize the list of sections
        secciones = []
        initial_speed = 0
        cumulative_time = 0

        # Create an instance of SimulatedSection for each segment
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
            
            # Set the start time for the section
            start_time = cumulative_time
            
            # Create a SimulatedSection instance
            seccion = SimulatedSection(
                coordinates, limit, initial_speed, start_time, self.bus, self.emissions)
            secciones.append(seccion)
            
            # Update the initial speed for the next section
            initial_speed = seccion.end_speed
            
            # Update the cumulative time
            cumulative_time = seccion.end_time
        
        # Consolidate results
        velocities = []
        start_times = []
        end_times = []
        
        for seccion in secciones:
            velocities.extend(seccion.velocities)
            start_times.append(seccion.start_time)
            end_times.append(seccion.end_time)

        # Return consolidated results along with the section start and end times
        return secciones
    
    def plot_altitude_profile(self, output_dir: str):
        """
        Plots the altitude profile of the route based on distance.
        Saves the plots in the output directory.

        Args
        --------
        output_dir: str
            The output directory
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
            start_altitude = section.start[2]
            end_altitude = section.end[2]

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
        plt.savefig(os.path.join(output_dir, "altitude_profile.png"))

    def plot_speed_profile(self, output_dir: str):
        """
        Plots the speed profile of the route based on distance.
        Saves the plots in the output directory.

        Args
        --------
        output_dir: str
            The output directory
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

            start_speed = section.start_speed
            end_speed = section.end_speed

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
        plt.savefig(os.path.join(output_dir, "speed_profile.png"))

    def plot_acceleration_profile(self, output_dir: str):
        """
        Plots the acceleration profile of the route based on distance.
        Saves the plots in the output directory.

        Args
        --------
        output_dir: str
            The output directory
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

        plt.grid(True)
        plt.savefig(os.path.join(output_dir, "acceleration_profile.png"))

    def plot_combined_profiles(self, output_dir: str):
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

            # Speed
            start_speed = section.start_speed
            end_speed = section.end_speed
            speeds.extend([start_speed, end_speed])

            # Acceleration
            acceleration = section.acceleration
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
        plt.savefig(os.path.join(output_dir, "combined_profiles.png"))

    def plot_map(self, output_dir):
        """
        Plots the route on an interactive map using folium.
        """
        # Create a folium map centered on the first coordinate
        if not self.sections:
            raise ValueError("No sections available to plot on the map.")

        start_coords = self.sections[0].start
        mapa = folium.Map(location=[start_coords[0], start_coords[1]], zoom_start=14)

        # Add lines to the map
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

        # Save the map to an HTML file
        mapa.save(os.path.join(output_dir, "2D_map.html"))
