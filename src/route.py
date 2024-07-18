import os

import folium
import pandas as pd

from section import Section


class Route:
    def __init__(self, filepath, bus):
        if filepath:
            self._data = self.__load_data(filepath)
            self.bus = bus
            self.sections = self.__process_sections(self._data)
        else:
            raise ValueError(
                "No file path provided. Please provide a file path to load data."
            )

    def __load_data(self, filepath: str):
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
        df = pd.read_csv(filepath)
        df = df.iloc[:, [2, 3, 4, 6, 8, 9]]
        df.columns = ["time", "latitude", "longitude", "altitude", "distance", "speed"]
        if df.iloc[0]["time"] == 0:
            first_non_zero_index = df[df["time"] != 0].index[0]
            df = df.iloc[first_non_zero_index - 1 :]
        return df

    def __process_sections(self, df: pd.DataFrame):
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

            section = Section(coordinates, speeds, timestamps, self.bus)
            sections.append(section)
        return sections

    def plot(self):
        """
        Plots the route in 3D using matplotlib
        """
        pass

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
        print(f"Map saved to {output_file}")
