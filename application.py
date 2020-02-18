"""
UTM:CSC148, Winter 2020
Assignment 1

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2020 Bogdan Simion, Michael Liut, Paul Vrbik
"""
import datetime
import csv
from typing import Dict, List, Tuple, Optional
from airport import Airport
from customer import Customer
from flight import Trip, FlightSegment
from visualizer import Visualizer

#############################################
# DO NOT DECLARE ANY OTHER GLOBAL VARIABLES!
#############################################

# AIRPORT_LOCATIONS: global mapping of an airport's IATA with their respective
#                    longitude and latitude positions.
# NOTE: This is used for our testing purposes, so it has to be populated in
# create_airports(), but you are welcome to use it as you see fit.
AIRPORT_LOCATIONS = {}

# DEFAULT_BASE_COST: Default rate per km for the base cost of a flight segment.
DEFAULT_BASE_COST = 0.1225


def import_data(file_airports: str, file_customers: str, file_segments: str,
                file_trips: str) -> Tuple[List[List[str]], List[List[str]],
                                          List[List[str]], List[List[str]]]:
    """ Opens all the data files <data/filename.csv> which stores the CSV data,
        and returns a tuple of lists of lists of strings. This contains the read
        in data, line-by-line, (airports, customers, flights, trips).

        Precondition: the dataset file must be in CSV format.
    """

    airport_log, customer_log, flight_log, trip_log = [], [], [], []

    airport_data = csv.reader(open(file_airports))
    customer_data = csv.reader(open(file_customers))
    flight_data = csv.reader(open(file_segments))
    trip_data = csv.reader(open(file_trips))

    for row in airport_data:
        airport_log.append(row)

    for row in flight_data:
        flight_log.append(row)

    for row in customer_data:
        customer_log.append(row)

    for row in trip_data:
        trip_log.append(row)

    return airport_log, flight_log, customer_log, trip_log


def create_customers(log: List[List[str]]) -> Dict[int, Customer]:
    """ Returns a dictionary of Customer IDs and their Customer instances, based
    on the customers from the input dataset from the <log>.

    Precondition:
        - The <log> list contains the input data in the correct format.
    >>> a = import_data('data/airports.csv', 'data/segments.csv','data/customers.csv', 'data/trips.csv')
    >>> create_customers(a[1])
    []
    """
    final = {}
    for line in log:
        final[int(line[0])] = Customer(int(line[0]), line[1], int(line[2]),
                                       line[3])
    return final


def create_flight_segments(log: List[List[str]])\
        -> Dict[datetime.date, List[FlightSegment]]:
    """ Returns a dictionary storing all FlightSegments, indexed by their
    departure date, based on the input dataset stored in the <log>.

    Precondition:
    - The <log> list contains the input data in the correct format.
    >>> a = import_data('data/airports.csv', 'data/segments.csv',
    'data/customers.csv', 'data/trips.csv')
    >>> create_flight_segments(a[2])
    []
    """
    month_days = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30,
                  10: 31, 11: 30, 12: 31}
    final = {}
    ids = {}
    a1 = import_data('data/airports.csv', 'data/segments.csv',
                     'data/customers.csv', 'data/trips.csv')
    airp = create_airports(a1[0])
    for airport in airp:
        ids[airport.get_airport_id()] = airport.get_location()
    for line in log:
        date1 = datetime.datetime
        date22 = datetime.datetime
        a = line[3]
        dep = line[4]
        arr = line[5]
        date1 = datetime.datetime(int(a[:4]), int(a[5:7]), int(a[8:]),
                                  int(dep[:2]), int(dep[3:]))
        if int(dep[:2]) >= int(arr[:2]):
            # if the return flight ends up not being in the same day
            if not month_days[date1.month] == date1.day:
                # if it isn't the last day of the month
                date22 = datetime.datetime(int(a[:4]), int(a[5:7]),
                                           int(a[8:]) + 1, int(arr[:2]),
                                           int(arr[3:]))
            else:
                # if it is the last day of the month
                date22 = datetime.datetime(int(a[:4]), int(a[5:7]) + 1, 1,
                                           int(arr[:2]), int(arr[3:]))

        elif int(dep[:2]) < int(arr[:2]):
            # if it lands the same day
            date22 = datetime.datetime(int(a[:4]), int(a[5:7]), int(a[8:]),
                                      int(arr[:2]), int(arr[3:]))

        if not datetime.date(int(a[:4]), int(a[5:7]), int(a[8:])) in final:
            # if the date doesn't already exist in the dic
            final[datetime.date(int(a[:4]), int(a[5:7]), int(a[8:]))] = \
                [FlightSegment(line[0], date1, date22, DEFAULT_BASE_COST,
                               float(line[6]), line[1], line[2],
                               (ids[line[1]], ids[line[2]]))]
        else:
            # if it already does
            final[datetime.date(int(a[:4]), int(a[5:7]), int(a[8:]))] += \
                [FlightSegment(line[0], date1, date22, DEFAULT_BASE_COST,
                               float(line[6]), line[1], line[2],
                               (ids[line[1]], ids[line[2]]))]
    return final


def create_airports(log: List[List[str]]) -> List[Airport]:
    """ Return a list of Airports with all applicable data, based
    on the input dataset stored in the <log>.

    Precondition:
    - The <log> list contains the input data in the correct format.
    >>> a = import_data('data/airports.csv', 'data/segments.csv',
    'data/customers.csv', 'data/trips.csv')
    >>> create_airports(a[0])
    []
    """
    final = []
    for line in log:
        final.append(Airport(line[0], line[1], (float(line[2]), float(line[3]))))
    return final


def load_trips(log: List[List[str]], customer_dict: Dict[int, Customer],
               flight_segments: Dict[datetime.date, List[FlightSegment]]) \
        -> List[Trip]:
    """ Creates the Trip objects and makes the bookings.

    Preconditions:
    - The <log> list contains the input data in the correct format.
    - the customers are already correctly stored in the <customer_dict>,
    indexed by their customer ID.
    - the flight segments are already correctly stored in the <flight_segments>,
    indexed by their departure date
    >>> a = import_data('data/airports.csv', 'data/segments.csv','data/customers.csv', 'data/trips.csv')
    >>> b = create_customers(a[1])
    >>> c = create_flight_segments(a[2])
    >>> load_trips(a[3], b ,c)
    []
    """
    final = []
    for line in log:
        booking_id = line[0]
        customer_id = int(line[1])
        dod = datetime.date(int(line[2][:4]), int(line[2][5:7]),
                                int(line[2][8:]))
        # extracting the arrivals and departures for
        temp_inter = []
        for i in range(len(line) - 1):
            if i >= 3 and i % 2 != 0:
                # if we are at the right index and odd i
                if i == 3:
                    # if we are at the very first dep
                    temp_inter.append(((line[i][3:6], line[i+2][2:5]),
                                       line[i+1][1:-2]))
                elif not (i + 2 > len(line) - 1) and not (i+2 > len(line)-1):
                    # If we are at an odd index and this is not the last dep
                    temp_inter.append(((line[i][2:5], line[i+2][2:5]),
                                       line[i+1][1:-2]))
        second_list = []
        for flight in flight_segments[dod]:
            # parsing through all the flights
            for segs in temp_inter:
                # parsing through my segments for this trip
                if flight.get_dep() == segs[0][0] and flight.get_arr() == segs[0][1]:
                    # if the arrivals and deps match
                    second_list.append((flight, segs[1]))
        final.append(customer_dict[customer_id].book_trip(booking_id,
                                                          second_list, dod))
    return final


if __name__ == '__main__':
    print("\n---------------------------------------------")
    print("Reading in all data! Processing...")
    print("---------------------------------------------\n")

    # input_data = import_data('data/airports.csv', 'data/customers.csv',
    #     'data/segments.csv', 'data/trips.csv')
    input_data = import_data('data/airports.csv', 'data/customers.csv',
                             'data/segments_small.csv', 'data/trips_small.csv')

    airports = create_airports(input_data[0])
    print("Airports Created! Still Processing...")
    flights = create_flight_segments(input_data[1])
    print("Flight Segments Created! Still Processing...")
    customers = create_customers(input_data[2])
    print("Customers Created! Still Processing...")
    print("Loading trips can take a while...")
    trips = load_trips(input_data[3], customers, flights)
    print("Trips Created! Opening Visualizer...\n")

    flights_len = 0
    for ky in flights:
        flights_len += len(flights[ky])

    print("---------------------------------------------")
    print("Some Statistics:")
    print("---------------------------------------------")
    print("Total airports in the dataset:", len(airports))
    print("Total flight segments in the dataset:", flights_len)
    print("Total customers in the dataset:", len(customers))
    print("Total trips in the dataset:", len(trips))
    print("---------------------------------------------\n")

    all_flights = [seg for tp in trips for seg in tp.get_flight_segments()]
    all_customers = [customers[cid] for cid in customers]

    V = Visualizer()
    V.draw(all_flights)

    while not V.has_quit():

        flights = V.handle_window_events(all_customers, all_flights)

        all_flights = []

        for flt in flights:
            all_flights.append(flt)

        V.draw(all_flights)

    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': [
            'python_ta', 'typing', 'csv', 'datetime', 'doctest',
            'visualizer', 'customer', 'flight', 'airport'
        ],
        'max-nested-blocks': 6,
        'allowed-io': [
            'create_customers', 'create_airports', 'import_data',
            'create_flight_segments', 'load_trips'
        ],
        'generated-members': 'pygame.*'
    })
