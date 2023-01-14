# Places Distance

This is a Python command line program that calculates the air distance (great circle distance) between all pairs of places. The program takes one optional integer argument n, and uses either a CSV file or n randomly generated places as input. The program then discards pairs having the same pair of places as another pair and prints out all place pairs and distances by ascending distance. On the last line, the program prints out the average distance and the place pair and corresponding distance having the distance closest to the average value.

## Setup
To run this program, you will need Python 3 installed on your machine. You can check if you have Python 3 installed by running the following command in your terminal:
```
python3 --version
```

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install pytest.

```bash
pip install pytest
```

## Usage

You can run the program from the command line by navigating to the directory where the program is located and running the following command:

```python
python3 main.py [n]
```
* If no argument is given, the program uses the file places.csv as input.
* If an argument is given, the program uses n randomly generated places as input.

The program will then calculate the air distance between all pairs of places and print out the pairs and distances in ascending order. The program will also print out the average distance and the place pair and corresponding distance having the distance closest to the average value.

To run the test cases run the following command:
```
pytest 
```

## Note
* Please make sure that the file places.csv is located in the same directory as the main.py file
* The program assumes that the csv file is in the correct format and has no missing data.

## Future Updates
* If the file doesnot exists, code that creates 'places.csv' directly.
* Make it faaster with the use of Cython.
