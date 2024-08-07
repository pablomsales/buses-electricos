import pandas as pd
import time
import os
from geopy.distance import great_circle
import overpy

# Start measuring time
start_time = time.time()

def get_closest_speed_limit(coordinates, radius):
    lat, lon = coordinates
    api = overpy.Overpass()

    # Fetch all ways and nodes
    result = api.query(f"""
        way(around:{radius},{lat},{lon}) ["maxspeed"];
        (._;>;);
        out body;
    """)

    closest_road = None
    min_distance = float('inf')
    
    for way in result.ways:
        # Calculate the distance to each node in the road
        for node in way.nodes:
            distance = great_circle(coordinates, (node.lat, node.lon)).meters
            if distance < min_distance:
                min_distance = distance
                closest_road = way

    if closest_road:
        # Extract and adjust the speed limit
        speed_limit_str = closest_road.tags.get("maxspeed", "n/a")
        try:
            speed_limit = int(speed_limit_str)
        except ValueError:
            speed_limit = 50  # Default to 50 if conversion fails
        
        # Cap speed limit at 50 km/h
        speed_limit = min(speed_limit, 50)

        return speed_limit
    else:
        return 50  # Default speed limit if no road is found

def process_csv(file_path, radius):
    # Read the CSV file
    df = pd.read_csv(file_path)

    results = []
    
    # Iterate over each row in the DataFrame
    for _, row in df.iterrows():
        lat = row['Latitud']
        lon = row['Longitud']
        coordinates = (lat, lon)
        speed_limit = get_closest_speed_limit(coordinates, radius)
        results.append({
            'Latitud': lat,
            'Longitud': lon,
            'Limite': speed_limit
        })

    return results

# Main logic
csv_file_path = os.path.join("data", "linea_d2_algoritmo.csv")
radius = 300  # Example radius
results = process_csv(csv_file_path, radius)

# Optionally, save the results to a new CSV file
results_df = pd.DataFrame(results)
results_df.to_csv(os.path.join("src", "simulation", "limits", "limits_linea_d2_algoritmo.csv"), index=False)

# End measuring time
end_time = time.time()
elapsed_time = end_time - start_time

# Print the elapsed time
print(f"Elapsed time: {elapsed_time:.2f} seconds")

print("Processing completed.")
