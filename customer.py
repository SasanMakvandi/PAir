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
from typing import List, Tuple, Dict, Optional
from flight import Trip

"""
    FF_Status: Dict[str, Tuple(int, int)] where the Tuple(status miles to reach, 
               discount for fares from the next trip (NOT flight segment) after 
               the status is achieved). The units are (Kilometres, Percent).
"""
FREQUENT_FLYER_STATUS = {"Prestige": (15000, -10), "Elite-Light": (30000, -15),
                         "Elite-Regular": (50000, -20),
                         "Super-Elite": (100000, -25)}

"""
    FREQUENT_FLYER_MULTIPLIER: the key is the type of cabin class (seat type), 
                               the value is the miles multiplier (status miles 
                               are calculated by multiplying the flight length 
                               by this miles multiplier).
"""
FREQUENT_FLYER_MULTIPLIER = {"Economy": 1, "Business": 5}

"""
    CLASS_MULTIPLIER: used (with the FlightSegment's base cost to determine the 
                      actual cost of the segment based on the class of flight: 
                      Tuple(int, int)] taken by the customer, where the 
                      Tuple(class, multiplier).
"""
CLASS_MULTIPLIER = {"Economy": 1, "Business": 2.5}


class Customer:
    """ A Customer of Python Air.

    === Public Attributes ===
    name:
        the customer's name (may include one or all:
        first, middle, and last).
    age:
        the customer's age.
    nationality:
        the customer's nationality (there are no dual citizens).
    all_flight_costs:
        the sum of all flight costs this customer has taken over
        the course of their existence.

    Representation Invariants:
        - trips are stored per customer forever.
        - miles/status are accumulated and never lost.
    """

    # === Private Attributes ===
    # _customer_id:
    #     this is a unique 6-digit customer identifier.
    # _ff_status:
    #     this is the customer's frequent flyer status.
    # _miles:
    #     this is the running tally of the customer's
    #     total qualifying miles for their status.
    # _trips:
    #     this stores the dictionary of Trips and their
    #     corresponding costs.

    name: str
    age: int
    nationality: str
    all_flight_costs: float
    _customer_id: int
    _trips: Dict[Trip, float]
    _ff_status: str
    _miles: int

    def __init__(self, cus_id: int, name: str, age: int, nat: str) -> None:
        """ A Customer of Python Air. """

        self.name = name
        self.age = age
        self.name = nat
        self._customer_id = cus_id
        self.all_flight_costs = 0.0
        self._trips = {}
        self._ff_status = ''
        self._miles = 0

    def get_id(self) -> int:
        """ Returns this customer's identification (ID). """

        return self._customer_id

    def get_trips(self) -> List[Trip]:
        """ Returns a list of Trips booked for this customer. """
        final = []
        for trip in self._trips:
            final.append(trip)
        return final

    def get_total_flight_costs(self) -> float:
        """ Returns this customer's total flight costs. """

        return self.all_flight_costs

    def get_cost_of_trip(self, trip_lookup: Trip) -> Optional[float]:
        """ Returns the cost of that Trip, otherwise None. """
        if trip_lookup in self._trips:
            return self._trips[trip_lookup]
        else:
            return None

    def get_ff_status(self) -> str:
        """ Returns this customer's frequent flyer status. """

        return self._ff_status

    def get_miles(self) -> int:
        """ Returns this customer's qualifying miles. """

        return self._miles

    def determine_ff_status(self) -> None:
        """
        determines the ff status
        """
        if self.get_miles() > 15000:
            self._ff_status = "Prestige"
        elif self.get_miles() > 30000:
            self._ff_status = "Elite-Light"
        elif self.get_miles() > 50000:
            self._ff_status = "Elite-Regular"
        elif self.get_miles() > 100000:
            self._ff_status = " Super-Elite"

    def book_trip(self, reservation_id: str,
                  segments: List[Tuple[FlightSegment, str]],
                  trip_date: datetime.date) -> Trip:
        """ Books the customer's trip and returns a Trip.

            <segments> are a List of Tuples, containing a (FlightSegment,
            seat_type) pair.

            Precondition: the customer is guaranteed to have a seat on each of
                          the <segments>.
        """
        temp = []
        cost = 0
        percent = 0.0
        for segi in segments:
            # list of the segments
            temp.append(segi[0])
            # actual miles of this segment
            self._miles += segi[0].get_length() * \
                           FREQUENT_FLYER_MULTIPLIER[segi[1]]
            # actual cost of this segment
            cost = segi[0].get_base_fare_cost() \
                                     * CLASS_MULTIPLIER[segi[1]]
            # checking the status to see if there is actually one or not
            if not self._ff_status == '':
                percent = abs(FREQUENT_FLYER_STATUS[self._ff_status][1]) / 100
            # updating the total cost
            cost += cost * percent
            self.all_flight_costs += cost * percent
            # updating the manifest
            segi[0].book_seat(self._customer_id, segi[1])
        # updating the ff status
        self.determine_ff_status()
        final = Trip(reservation_id, self._customer_id, trip_date, temp)
        self._trips[final] = cost
        return final

    def cancel_trip(self, canceled_trip: Trip,
                    segments: List[Tuple[FlightSegment, str]]) -> None:
        """ Cancels this customer's Trip.

            <segments> are a List of Tuples, containing the (FlightSegment,
            seat_type) pair.

            Precondition: the <canceled_trip> must be a valid Trip that this
                          customer has booked.
        """
        temp = []
        percent = 0.0
        for flight in segments:
            if flight in canceled_trip.get_flight_segments():
                temp.append(flight)
        for segi in temp:
            cost = segi[0].get_base_fare_cost() \
                   * CLASS_MULTIPLIER[segi[1]]
            if not self._ff_status == '':
                percent = abs(FREQUENT_FLYER_STATUS[self._ff_status][1]) / 100
                cost = cost * percent
            self.all_flight_costs -= cost + 100
            segi[0].cancel_seat(self._customer_id)


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': [
            'python_ta',
            'typing',
            'doctest',
            'flight',
            '__future__',
        ],
        'max-attributes': 8,
    })
