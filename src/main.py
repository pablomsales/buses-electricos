import os
from Route import Route


def main():

    data = os.path.join("data", "datos_test.csv")
    route = Route(data)

if __name__ == "__main__":
    main()
