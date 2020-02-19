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
from typing import List
from customer import Customer
from flight import FlightSegment
# from time import sleep


class Filter:
    """ A class for filtering flight segments based on some criterion.

        This is an abstract class. Only subclasses should be instantiated.
    """
    def __init__(self) -> None:
        pass

    def apply(self, customers: List[Customer], data: List[FlightSegment],
              filter_string: str) -> List[FlightSegment]:
        """ Returns a list of all flight segments from <data>, which match the
            filter specified in <filter_string>.

            The <filter_string> is provided by the user through the visual
            prompt, after selecting this filter.

            The <customers> is a list of all customers from the input dataset.

            If the filter has no effect or the <filter_string> is invalid then
            return the same flights segments from the <data> input.

            Precondition:
                - <customers> contains the list of all customers from the input
                  dataset
                - all flight segments included in <data> are valid segments
                  from the input dataset
        """
        raise NotImplementedError

    def __str__(self) -> str:
        """ Returns a description of this filter to be displayed in the UI menu
        """
        raise NotImplementedError


class ResetFilter(Filter):
    """ A class for resetting all previously applied filters, if any. """
    def apply(self, customers: List[Customer], data: List[FlightSegment],
              filter_string: str) -> List[FlightSegment]:
        """ Reset all of the applied filters. Returns a List containing all the
            flight segments corresponding to all trips of <customers>.

            The <data>, <customers>, and <filter_string> arguments for this
            type of filter are ignored.
        """
        final = []
        for cus in customers:
            for trip in cus.get_trips():
                for seg in trip.get_flight_segments():
                    final.append(seg)
        return final

    def __str__(self) -> str:
        """ Returns a description of this filter to be displayed in the UI menu.
            Unlike other __str__ methods, this one is required!
        """
        return "Reset all of the filters applied so far (if any)!"


class CustomerFilter(Filter):
    """ A class for selecting the flight segments for a given customer. """
    def apply(self, customers: List[Customer], data: List[FlightSegment],
              filter_string: str) -> List[FlightSegment]:
        """ Returns a list of all flight segments from <data> made or received
            by the customer with the id specified in <filter_string>.

            The <customers> list contains all customers from the input dataset.

            The filter string is valid if and only if it contains a valid
            customer ID.

            If the filter string is invalid, do the following:
              1. return the original list <data>, and
              2. ensure your code does not crash.
        """
        NUMS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        for el in filter_string:
            if el not in NUMS:
                return data
        final = []
        temp_list = []
        for cus in customers:
            if cus.get_id() == int(filter_string):
                for trip in cus.get_trips():
                    for seg in trip.get_flight_segments():
                        temp_list.append(seg)
        for flight in data:
            if flight in temp_list:
                final.append(flight)
        return final

    def __str__(self) -> str:
        """ Returns a description of this filter to be displayed in the UI menu.
            Unlike other __str__ methods, this one is required!
        """
        return "Filter events based on customer ID"


class DurationFilter(Filter):
    """ A class for selecting only the flight segments lasting either over or
        under a specified duration.
    """
    def apply(self, customers: List[Customer], data: List[FlightSegment],
              filter_string: str) -> List[FlightSegment]:
        """ Returns a list of all flight segments from <data> with a duration of
            under or over the time indicated in the <filter_string>.

            The <customers> list contains all customers from the input dataset.

            The filter string is valid if and only if it contains the following
            input format: either "Lxxxx" or "Gxxxx", indicating to filter
            flight segments less than xxxx or greater than xxxx minutes,
            respectively.

            If the filter string is invalid, do the following:
              1. return the original list <data>, and
              2. ensure your code does not crash.
        """
        final = []
        NUMS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        if ((filter_string[:1] != 'L') or (filter_string[:1] != 'G')) \
                and len(filter_string[1:]) != 4:
            return data
        for el in filter_string[1:]:
            if el not in NUMS:
                return data
        time = filter_string[:1]
        mins = int(filter_string[1:])
        if time == 'L':
            for flight in data:
                time2 = int(flight.get_duration().hour * 60 +
                            flight.get_duration().minute)
                if time2 < mins:
                    final.append(flight)
        elif time == 'G':
            for flight in data:
                time2 = int(flight.get_duration().hour * 60 +
                            flight.get_duration().minute)
                if time2 > mins:
                    final.append(flight)
        return final

    def __str__(self) -> str:
        """ Returns a description of this filter to be displayed in the UI menu
        """
        return "Filter flight segments based on duration; " \
               "L#### returns flight segments less than specified length, " \
               "G#### for greater "


class LocationFilter(Filter):
    """ A class for selecting only the flight segments which took place within
        a specific area.
    """
    def apply(self, customers: List[Customer], data: List[FlightSegment],
              filter_string: str) -> List[FlightSegment]:
        """ Returns a list of all flight segments from <data>, which took place
            within a location specified by the <filter_string> (the IATA
            departure or arrival airport code of the segment was
            <filter_string>).

            The <customers> list contains all customers from the input dataset.

            The filter string is valid if and only if it contains a valid
            3-string IATA airport code. In the event of an invalid string:
              1. return the original list <data>, and
              2. your code must not crash.
        """
        final = []
        airports = []
        for cus in customers:
            for trips in cus.get_trips():
                for seg in trips.get_flight_segments():
                    airports.append(seg.get_arr())
                    airports.append(seg.get_dep())
        for el in filter_string:
            if not isinstance(el, str):
                return data
        if len(filter_string) == 3 and filter_string in airports:
            for flight in data:
                if flight.get_dep() == filter_string or flight.get_arr() == \
                        filter_string:
                    final.append(flight)
        return final

    def __str__(self) -> str:
        """ Returns a description of this filter to be displayed in the UI menu.
            Unlike other __str__ methods, this one is required!
        """
        return "Filter flight segments based on an airport location;\n" \
               "DXXX returns flight segments that depart airport XXX,\n"\
               "AXXX returns flight segments that arrive at airport XXX\n"


class DateFilter(Filter):
    """ A class for selecting all flight segments that departed and arrive
    between two dates (i.e. "YYYY-MM-DD/YYYY-MM-DD" or "YYYY MM DD YYYY MM DD").
    """
    def apply(self, customers: List[Customer], data: List[FlightSegment],
              filter_string: str) -> List[FlightSegment]:
        """ Returns a list of all flight segments from <data> that have departed
            and arrived between the range of two dates indicated in the
            <filter_string>.

            The <customers> list contains all customers from the input dataset.

            The filter string is valid if and only if it contains the following
            input format: either "YYYY-MM-DD/YYYY-MM-DD" or
            "YYYY MM DD YYYY MM DD", indicating to filter flight segments
            between the first occurrence of YYYY-MM-DD and the second occurence
            of YYYY-MM-DD.

            If the filter string is invalid, do the following:
              1. return the original list <data>, and
              2. ensure your code does not crash.
        """
        ints = [[filter_string[:4], filter_string[5:7], filter_string[8:10],
                 filter_string[11:15], filter_string[16:18],
                 filter_string[19:]],
                ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']]
        for el in ints[0]:
            for num in el:
                if num not in ints[1]:
                    return data
        if not((filter_string[4:5] == '-' or ' ') and
               (filter_string[7:8] == '-' or ' ') and
               (filter_string[10:11] == '/' or ',' or ' ') and
               (filter_string[15:16] == '-' or ' ') and
               (filter_string[18:19] == '-' or ' ')):
            return data

        import datetime
        final = []
        date1 = datetime.date(int(filter_string[:4]), int(filter_string[5:7]),
                              int(filter_string[8:10]))
        date2 = datetime.date(int(filter_string[11:15]),
                              int(filter_string[16:18]),
                              int(filter_string[19:]))
        for flights in data:
            aar = datetime.date(flights.get_times()[1].year,
                                flights.get_times()[1].month,
                                flights.get_times()[1].day)
            dep = datetime.date(flights.get_times()[0].year,
                                flights.get_times()[0].month,
                                flights.get_times()[0].day)
            if date1 <= aar <= date2 or date1 <= dep <= date2:
                final.append(flights)
        return final

    def __str__(self) -> str:
        """ Returns a description of this filter to be displayed in the UI menu.
            Unlike other __str__ methods, this one is required!
        """
        return "Filter flight segments based on dates; " \
               "'YYYY-MM-DD/YYYY-MM-DD' or 'YYYY-MM-DD,YYYY-MM-DD'"


class TripFilter(Filter):
    """ A class for selecting the flight segments for a trip. """
    def apply(self, customers: List[Customer], data: List[FlightSegment],
              filter_string: str) -> List[FlightSegment]:
        """ Returns a list of all flight segments from <data> where the
            <filter_string> specified the trip's reservation id.

            The <customers> list contains all customers from the input dataset.

            The filter string is valid if and only if it contains a valid
            Reservation ID.

            If the filter string is invalid, do the following:
              1. return the original list <data>, and
              2. ensure your code does not crash.
        """
        allowed = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                   'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                   'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        for el in filter_string:
            if el not in allowed:
                return data
        final = []
        temp = []
        for cus in customers:
            for trips in cus.get_trips():
                if trips.get_reservation_id() == filter_string:
                    temp += trips.get_flight_segments()
        for segment in data:
            if segment in temp:
                final.append(segment)
        return final

    def __str__(self) -> str:
        """ Returns a description of this filter to be displayed in the UI menu.
            Unlike other __str__ methods, this one is required!
        """
        return "Filter events based on a reservation ID"


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': [
            'python_ta', 'typing', 'datetime', 'doctest',
            'customer', 'flight', 'time'
        ],
        'max-nested-blocks': 5,
        'allowed-io': ['apply', '__str__']
    })
