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
from __future__ import annotations
from typing import Dict, List, Optional, Tuple
import datetime

# Global Airplane Seat Type capacity
AIRPLANE_CAPACITY = {"Economy": 150, "Business": 22}


class FlightSegment:
    """ A FlightSegment offered by the airline system.

    === Public Attributes ===
    flight_id:
        a unique identifier for this flight.
    time:
        a tuple containing the departure and arrival time of a segment.
    fare_cost:
        the base cost of the fare (i.e. $0.1225/km).
    seat_capacity:
        the class of seat and total number of seats available on a specific
        segment.
    seat_availability:
        the class of seat and number of seats still available on a specific
        segment.
    flight_duration:
        the amount of time it takes for this flight segment to complete.
    flight_length:
        the number of kilometres between the dep_loc and arr_loc.
    dep_loc:
        the unique 3-digit (IATA) airport identifier of where the flight
        segment is departing (i.e. leaving from).
    arr_loc:
        the unique 3-digit (IATA) airport identifier of where the flight
        segment is landing (i.e. arriving to).
    long_lat:
        a tuple of tuples, containing the longitude and latitude of the
        departure and arrival destinations.

    === Representation Invariants ===
        -  flight_duration >= 0
        -  flight_length >= 0
        -  the value for seat_available.keys() must all be >= 0
           (i.e. they cannot be negative)
        -  dep_loc and arr_loc must be exactly three characters [A-Z]
           and are assumed to be valid and distinct IATA airport codes.
    """

    # === Private Attributes ===
    # _manifest:
    #      a list of tuples containing all customers' ID and type of flight
    #      class that they've taken (e.g. economy).

    flight_id: str
    time: Tuple[datetime.datetime, datetime.datetime]
    fare_cost: float
    seat_capacity: Dict[str, int]  # str: class, int: seats_available
    seat_availability: Dict[str, int]  # str: class, int: seats_available
    flight_duration: Optional[datetime.time]  # to allow for None at __init__
    flight_length: float
    dep_loc: str
    arr_loc: str
    long_lat: Tuple[Tuple[float, float], Tuple[float, float]]
    _manifest: List[Tuple[int, str]]  # (customer_id, seat_type)

    def __init__(self, fid: str, dep: datetime.datetime, arr: datetime.datetime,
                 cost: float, length: float, dep_loc: str, arr_loc: str,
                 long_lat: Tuple[Tuple[float, float],
                                 Tuple[float, float]]) -> None:
        """ Initialize a FlightSegment object based on the parameters specified.
        """

        """
        The base cost of the flight is calculated at a rate of $0.2325/km. This
        cost will change depending on their booking class (i.e. utilizing the
        CLASS_MULTIPLIER).
        """

        # TODO

    def __repr__(self) -> str:
        return ("[" + str(self.flight_id) + "]:" + str(self.dep_loc) + "->" +
                str(self.arr_loc))

    def get_length(self) -> float:
        """ Returns the length, in KMs, of this flight segment. """

        # TODO

    def get_times(self) -> Tuple[datetime.datetime, datetime.datetime]:
        """ Returns the (departure, arrival) time of this flight segment. """

        # TODO

    def get_arr(self) -> str:
        """ Returns the arrival airport (i.e. the IATA). """

        # TODO

    def get_dep(self) -> str:
        """ Returns the departure airport (i.e. the IATA). """

        # TODO

    def get_fid(self) -> str:
        """ Returns the flight identifier. """

        # TODO

    def get_long_lat(self) -> Tuple[Tuple[float, float], Tuple[float, float]]:
        """ Returns the longitude and latitude of a FlightSegment,
            specifically like this: ((LON1, LAT1), (LON2, LAT2)).
        """

        # TODO

    def get_duration(self) -> datetime.time:
        """ Returns the duration of the flight. """

        # TODO

    def get_fare_price(self) -> float:
        """ Returns the base fair price for this flight segment. """

        # TODO

    def check_manifest(self, cid: int) -> bool:
        """ Returns True if a certain customer <cid> has booked a seat
            on this specific flight, otherwise False.
        """

        # TODO

    def check_seat_class(self, cid: int) -> Optional[str]:
        """ Checks the manifest to see what class of cabin a certain customer
            (based on their <cid>) has booked. None is returned in the event
            there is no seat booked for that <cid>.
        """

        # TODO

    def book_seat(self, cid: int, seat_type: str) -> None:
        """ Book a seat of the given <seat_type> for the customer <cid>.
            If that customer is already booked, do nothing. If the seat
            type is different, and it is available, make the change.
        """

        # TODO

    def cancel_seat(self, cid: int) -> None:
        """	If a seat has already been booked by <cid>, cancel the booking
            and restore the seat's availability. Otherwise, do nothing and
            return None.
        """

        # TODO


# ------------------------------------------------------------------------------
class Trip:
    """ A Trip is composed of FlightSegment(s) which makes up a customer's
        itinerary.

    === Public Attributes ===
    reservation_id:
         a unique identifier for this trip.
    customer_id:
         the unique identifier of the customer who booked this trip.
    trip_departure:
         the date in which this trip was booked.
    """
    # === Private Attributes ===
    # _flights:
    #      a list of all flight segments for this particular trip
    reservation_id: str
    customer_id: int
    trip_departure: datetime.date
    _flights: List[FlightSegment]

    def __init__(self, rid: str, cid: int, trip_date: datetime.date,
                 flight_segments: List[FlightSegment]) -> None:
        """ Initializes a trip object given the specified parameters. """

        # TODO

    def get_flight_segments(self) -> List[FlightSegment]:
        """ Returns a list of all Flight Segments part of this booking. """

        # TODO

    def get_reservation_id(self) -> str:
        """ Returns this Trip's Reservation ID. """

        # TODO

    def get_in_flight_time(self) -> int:
        """ Returns the amount of time (in minutes) the trip is spent in
            flight (i.e. the time in the air only).
        """

        # TODO

    def get_total_trip_time(self) -> int:
        """ Returns the amount of time (in minutes) the trip is takes,
            including all transit time (i.e. including waiting for the next
            flight on a layover).
        """

        # TODO


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': [
            'python_ta', 'typing', 'doctest',
            'datetime', '__future__'
        ],
        'max-attributes': 11,
        'max-args': 9
    })
