import pytest
from src.main import Places, Place
import io
import sys


@pytest.fixture(autouse=True)
def test_read_csv():
    """
    Test that the read_csv method correctly reads and parses the data from a CSV file
    """
    places = Places([])
    places.read_csv('../src/places.csv')
    assert len(places.places) == 10
    assert places.places[0].name == 'Alta'
    assert places.places[0].latitude == 69.96887
    assert places.places[0].longitude == 23.27165


def test_generate_random():
    """
      Test that the generate_random method correctly generates the specified number of random places
    """
    places = Places([])
    places.generate_random(5)
    assert len(places.places) == 5
    assert all(isinstance(p, Place) for p in places.places)


def test_air_distance():
    """
    Test that the air_distance method correctly calculates the air distance (great circle distance) between two places
    """
    places = Places([])
    places.places = [Place('A', 0, 0), Place('B', 0, 1), Place('C', 1, 0), Place('D', 1, 1)]
    assert places.air_distance(places.places[0], places.places[1]) == 111.19492664455874
    assert places.air_distance(places.places[0], places.places[2]) == 111.19492664455874
    assert places.air_distance(places.places[0], places.places[3]) == 157.24938127194397


def test_read_csv_file_not_found():
    """
    Test that the read_csv method raises a FileNotFoundError when the specified CSV file is not found
    """
    places = Places([])
    with pytest.raises(FileNotFoundError):
        places.read_csv('not_found.csv')


def test_generate_random_negative():
    """
    Test that the generate_random method raises a ValueError when a negative number is passed as an argument
    """
    places = Places([])
    with pytest.raises(ValueError):
        places.generate_random(-1)


def test_air_distance_same_place():
    """
    Test that the air_distance method returns 0 when the same place is passed as both arguments
    """

    places = Places([])
    p1 = Place('A', 0, 0)
    assert places.air_distance(p1, p1) == 0.0


def test_all_pairs_distance_no_places():
    """
     Test that the all_pairs_distance method returns an empty list when there are no places in the Places object
    """
    places = Places([])
    assert places.all_pairs_distance() == []


def test_print_pairs():
    """
    Test that the print_pairs method correctly prints out all place pairs and distances by ascending distance
    in the correct format
    """
    places = Places([])
    places.places = [Place('A', 0, 0), Place('B', 0, 1), Place('C', 1, 0), Place('D', 1, 1)]
    distances = places.all_pairs_distance()
    # redirect the output to a string buffer
    sys.stdout = io.StringIO()
    places.print_pairs()
    output = sys.stdout.getvalue()
    output_lines = output.strip().split('\n')
    for i in range(len(distances)):
        assert output_lines[i] == f"{distances[i][0].name:<25} {distances[i][1].name:<25} {distances[i][2]:.1f} km"
    # reset the output to the console
    sys.stdout = sys.__stdout__


def test_print_average_distance():
    """
    Test that the print_average_distance method correctly prints out the average distance and the place pair and
    corresponding distance having the distance closest to the average value
    """
    places = Places([])
    places.places = [Place('A', 0, 0), Place('B', 0, 1), Place('C', 1, 0), Place('D', 1, 1)]
    distances = places.all_pairs_distance()
    avg = sum(d[2] for d in distances) / len(distances)
    closest = min(distances, key=lambda d: abs(d[2] - avg))
    # redirect the output to a string buffer
    sys.stdout = io.StringIO()
    places.print_average_distance()
    output = sys.stdout.getvalue().strip()
    assert output == f"Average distance: {avg:.1f} km. Closest pair: {closest[0].name} - {closest[1].name} {closest[2]:.1f} km."
    # reset the output to the console
    sys.stdout = sys.__stdout__


def test_all_pairs_distance():
    """
    Test that the all_pairs_distance method correctly calculates the air distance between all pairs of places,
    discards pairs having the same pair of places as another pair and returns the correct number of pairs.
    """
    places = Places([])
    places.places = [Place('A', 0, 0), Place('B', 0, 1), Place('C', 1, 0), Place('D', 1, 1)]
    distances = places.all_pairs_distance()
    n = len(places.places)
    assert len(distances) == (n * (n - 1)) / 2
