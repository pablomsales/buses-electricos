import os
from route import Route


def main():

    data = os.path.join("data", "datos_test.csv")
    route = Route(data)
    route.plot_map()

if __name__ == "__main__":
    main()
