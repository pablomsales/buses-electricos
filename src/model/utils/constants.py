AIR_DENSITY = 1.225
CO2_CONVERSION_FACTOR = 2.64
GRAVITY = 9.81
MAX_ACCELERATION = 1.5  # m/s^2
MAX_DECELERATION = -1.0  # m/s^2, note this is negative

fuels_lhv = {
    "gasoline": 3.1536e7,  # J/L
    "diesel": 3.58e7,
    "propane": 2.5e7,
    "natural_gas": 3.6e7,
    "E85": 2.4e7,
    "E100": 2.68e7,
}

euro_standards = {
    "EURO_1": {
        "NOx": 8.0,  # g/kWh
        "CO": 4.5,  # g/kWh
        "HC": 1.1,  # g/kWh
        "PM": 0.36,  # g/kWh
    },
    "EURO_2": {
        "NOx": 7.0,
        "CO": 4.0,
        "HC": 1.1,
        "PM": 0.15,
    },
    "EURO_3": {
        "NOx": 5.0,
        "CO": 2.1,
        "HC": 0.66,
        "PM": 0.10,
    },
    "EURO_4": {
        "NOx": 3.5,
        "CO": 1.5,
        "HC": 0.46,
        "PM": 0.02,
    },
    "EURO_5": {
        "NOx": 2.0,
        "CO": 1.5,
        "HC": 0.46,
        "PM": 0.02,
    },
    "EURO_6": {
        "NOx": 0.4,
        "CO": 1.5,
        "HC": 0.13,
        "PM": 0.01,
    },
}
