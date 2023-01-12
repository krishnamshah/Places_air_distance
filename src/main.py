import csv
import random
import math
from typing import List


class Place:
    """
    A class that represents a place with a name, latitude and longitude.
    """

    def __init__(self, name: str, latitude: float, longitude: float):
        """
        Initialize the Place class with a name, latitude, and longitude.

        :param name: the name of the place
        :param latitude: the latitude of the place
        :param longitude: the longitude of the place
        """
        self.name = name
        self.latitude = latitude
        self.longitude = longitude


class Places:
    """
    A class that represents a list of places and provides methods for
    reading from a CSV file, generating random places, calculating
    the air distance between pairs of places, and printing the pairs
    and distances.
    """

    def __init__(self, places: List[Place]):
        """
        Initialize the Places class with a list of Place objects.
        :param places: a list of Place objects
        """
        self.places = places

    def read_csv(self, file_name: str):
        """
        Read places from a CSV file and add them to the list of places.

        :param file_name: the path of the CSV file
        :raises: FileNotFoundError if the file does not exist
        """
        with open(file_name) as file:
            reader = csv.reader(file)
            next(reader)  # skip header
            for row in reader:
                name, lat, lon = row
                self.places.append(Place(name, float(lat), float(lon)))

    def generate_random(self, n: int):
        """
        Generate n randomly generated places and add them to the list of places.

        :param n: the number of places to generate
        :raises: ValueError if n is negative
        """
        if n < 0:
            raise ValueError("n should be a positive integer.")
        for _ in range(n):
            lat = random.uniform(-90, 90)
            lon = random.uniform(-180, 180)
            self.places.append(Place(f'Place {_}', lat, lon))

    def air_distance(self, p1: Place, p2: Place) -> float:
        """
        Calculate the air distance (great circle distance) between two places.

        :param p1: the first place
        :param p2: the second place
        :return: the air distance between the two places
        """
        r = 6371  # Earth radius in km
        lat1, lon1, lat2, lon2 = math.radians(p1.latitude), math.radians(p1.longitude), math.radians(
            p2.latitude), math.radians(p2.longitude)
        dlat, dlon = lat2 - lat1, lon2 - lon1
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return r * c

    def all_pairs_distance(self):
        """
        Calculate the air distance between all pairs of places.
        Discard pairs having the same pair of places as another pair.

        :return: a list of tuples, where each tuple contains two Place objects
                 and the air distance between them
        """
        distances = []
        for i, p1 in enumerate(self.places):
            for p2 in self.places[i + 1:]:
                distances.append((p1, p2, self.air_distance(p1, p2)))
        return sorted(distances, key=lambda x: x[2])

    def print_pairs(self):
        """
        Print out all place pairs and distances by ascending distance,
        lines column aligned and formatted like this:
        Someplace Otherplace 152.6 km
        """
        for p1, p2, d in self.all_pairs_distance():
            print(f"{p1.name:<25} {p2.name:<25} {d:.1f} km")

    def print_average_distance(self):
        """
        Print out the average distance and the place pair and corresponding
        distance having the distance closest to the average value, like this:
        Average distance: 321.8 km. Closest pair: Thisplace – Thatplace 312.5 km.
        """
        distances = [d for p1, p2, d in self.all_pairs_distance()]
        avg = sum(distances) / len(distances)
        closest_pair = min(self.all_pairs_distance(), key=lambda x: abs(x[2] - avg))
        print(
            f"Average distance: {avg:.1f} km. Closest pair: {closest_pair[0].name} - {closest_pair[1].name} {closest_pair[2]:.1f} km.")


if __name__ == "__main__":
    import sys

    places = Places([])
    if len(sys.argv) == 1:
        places.read_csv('places.csv')
    elif sys.argv[1].isdigit():
        n = int(sys.argv[1])
        places.generate_random(n)
    else:
        print(f"Invalid argument: {sys.argv[1]}. Please provide a positive integer.")
        sys.exit()
    places.print_pairs()
    places.print_average_distance()
