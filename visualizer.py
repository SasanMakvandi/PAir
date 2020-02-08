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
import os
import threading
import math
import time
from typing import List, Tuple, Any, Union, Callable
from tkinter import *
import pygame
from customer import Customer
from flight import FlightSegment
from filter import CustomerFilter, DateFilter, DurationFilter
from filter import LocationFilter, ResetFilter, TripFilter

""" ======================== Module Description ================================

    This file contains the Visualizer class, which is responsible for 
    interacting with PyGame, the graphics library we're using for this 
    assignment. There is quite a bit in this file, but you are not 
    responsible for most of it.

    It also contains the Map class, which is responsible for converting between
    long/lat coordinates and pixel coordinates on the PyGame window.

    DO NOT CHANGE ANY CODE IN THIS FILE, unless instructed in the handout.
"""

LINE_COLOUR = (0, 64, 125)
WHITE = (255, 255, 255)

# Map's Top-Left Coordinates (long, lat)
MAP_MIN = (-180.0, 90.0)
# Map's Bottom-Right Coordinates (long, lat)
MAP_MAX = (180.0, -90.0)

# Window Size
SCREEN_SIZE = (1000, 700)

# File Image Location
MAP_FILE = 'images/map.png'


class Visualizer:
    """ Visualizer for the current state of a simulation.

    === Public Attributes ===
        r: the Tk object for the main window
    """
    # === Private attributes ===
    # _screen: the PyGame window that is shown to the user.
    # _mouse_down: whether the user is holding down a mouse button
    #   on the PyGame window.
    # _map: the Map object responsible for converting between longitude/latitude
    #   coordinates and the pixels of the visualization window.
    r: Tk
    _ui_screen: pygame.Surface
    _screen: pygame.Surface
    _mouse_down: bool
    _map: 'Map'
    _quit: bool

    def __init__(self) -> None:
        """ Initialize this visualizer. """
        self.r = Tk()
        Label(self.r, text="Python Air\'s Frequent Flyer System")\
            .grid(row=0, column=0)
        self.r.title("Python Air\'s Frequent Flyer System")
        pygame.init()

        self._ui_screen = pygame.display.set_mode((SCREEN_SIZE[0] + 200,
                                                   SCREEN_SIZE[1]),
                                                  pygame.HWSURFACE |
                                                  pygame.DOUBLEBUF)

        # Add the text along the side, displaying the command keys for filters
        self._ui_screen.fill((125, 125, 125))
        font = pygame.font.SysFont(None, 25)
        self._ui_screen.blit(font.render("FILTER KEYBINDS", True, WHITE),
                             (SCREEN_SIZE[0] + 10, 50))
        self._ui_screen.blit(font.render("C: Customer ID", True, WHITE),
                             (SCREEN_SIZE[0] + 10, 100))
        self._ui_screen.blit(font.render("D: Duration", True, WHITE),
                             (SCREEN_SIZE[0] + 10, 150))
        self._ui_screen.blit(font.render("L: Location", True, WHITE),
                             (SCREEN_SIZE[0] + 10, 200))
        self._ui_screen.blit(font.render("T: Trip", True, WHITE),
                             (SCREEN_SIZE[0] + 10, 250))
        self._ui_screen.blit(font.render("Y: Date", True, WHITE),
                             (SCREEN_SIZE[0] + 10, 300))

        self._ui_screen.blit(font.render("S: Summary of Trip", True, WHITE),
                             (SCREEN_SIZE[0] + 10, 500))

        self._ui_screen.blit(font.render("R: Reset Filters", True, WHITE),
                             (SCREEN_SIZE[0] + 10, 600))
        self._ui_screen.blit(font.render("Q: Quit Application", True, WHITE),
                             (SCREEN_SIZE[0] + 10, 650))

        self._screen = self._ui_screen.subsurface((0, 0), SCREEN_SIZE)
        self._screen.fill(WHITE)
        self._mouse_down = False
        self._map = Map(SCREEN_SIZE)

        # Initial render
        self.draw([])
        self._quit = False

    def draw(self, long_lats: List[FlightSegment]) -> None:
        """ Render the <long_lats> to the screen. """

        # Draw the background map onto the screen
        self._screen.fill(WHITE)
        self._screen.blit(self._map.get_current_view(), (0, 0))

        # Add all of the objects onto the screen
        self._map.render_objects(long_lats, self._screen)

        # Show the new image
        pygame.display.flip()

    def has_quit(self) -> bool:
        """ Returns True if the program has received the quit command. """
        return self._quit

    def handle_window_events(self, customers: List[Customer],
                             drawables: List[FlightSegment])\
            -> List[FlightSegment]:
        """ Handle any user events triggered through the PyGame window.
            The <drawables> are the objects currently displayed, while the
            <customers> list contains all customers from the input data. Returns 
            a new list of FlightSegment, according to user input actions.
        """
        new_drawables = drawables
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._quit = True
            elif event.type == pygame.KEYDOWN:
                f = None
                num_threads = 1

                if event.unicode.lower() == "d":
                    f = DurationFilter()
                elif event.unicode.lower() == "l":
                    f = LocationFilter()
                elif event.unicode.lower() == "c":
                    f = CustomerFilter()
                elif event.unicode.lower() == "y":
                    f = DateFilter()
                elif event.unicode.lower() == "t":
                    f = TripFilter()
                elif event.unicode.lower() == "s":
                    self.display_summary(customers)
                elif event.unicode.lower() == "r":
                    f = ResetFilter()
                    num_threads = 1
                elif event.unicode.lower() == "q":
                    self._quit = True

                if f is not None:
                    def result_wrapper(fun: Callable[[List[Customer],
                                                      List[FlightSegment], str],
                                                     List[FlightSegment]],
                                       customers_lst: List[Customer],
                                       data: List[FlightSegment],
                                       filter_string: str, res: List) -> None:
                        """ A final wrapper to return the result of the
                            operation
                        """
                        res.append(fun(customers_lst, data,
                                       filter_string.upper()))

                    def threading_wrapper(customers_lst: List[Customer],
                                          flight_data: List[FlightSegment],
                                          filter_string: str
                                          ) -> List[FlightSegment]:
                        """ A wrapper for the application of filters with
                            threading
                        """
                        chunk_sz_flights = math.ceil(
                            (len(flight_data) + num_threads - 1) / num_threads)
                        print("Num_threads:", num_threads)
                        print("Chunk_flights:", chunk_sz_flights)
                        threads = []
                        results = []
                        for i in range(num_threads):
                            res = []
                            results.append(res)
                            t = threading.Thread(
                                target=result_wrapper,
                                args=(f.apply, customers_lst,
                                      flight_data[i * chunk_sz_flights:
                                                  (i + 1) * chunk_sz_flights],
                                      filter_string.upper(), res))
                            t.daemon = True
                            t.start()
                            threads.append(t)
                            # f.apply(customers_lst, flight_data,
                            #         filter_string.upper())
                        # Wait to finish
                        for t in threads:
                            t.join()

                        # Now reconstruct the data
                        new_data = []
                        for res in results:
                            new_data.extend(res[0])
                        return new_data

                    new_drawables = self.entry_window(str(f), customers,
                                                      drawables,
                                                      threading_wrapper)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self._mouse_down = True
                elif event.button == 4:
                    self._map.zoom(-0.1)
                elif event.button == 5:
                    self._map.zoom(0.1)
            elif event.type == pygame.MOUSEBUTTONUP:
                self._mouse_down = False
            elif event.type == pygame.MOUSEMOTION:
                if self._mouse_down:
                    self._map.pan(pygame.mouse.get_rel())
                else:
                    pygame.mouse.get_rel()

        return new_drawables

    def entry_window(self, field: str, customers: List[Customer],
                     drawables: Union[List[Customer], List[FlightSegment]],
                     callback: Callable[[List[Customer],
                                         List[FlightSegment], str],
                                        List[FlightSegment]]) \
            -> Union[List[FlightSegment], List[Any]]:
        """ Creates a pop-up window for the user to enter input text, and
            applies the <callback> function onto the <drawables>
        """
        new_drawables = []
        m = Tk()
        m.title("Filter")
        Label(m, text=field).grid(row=0)

        el = Entry(m)
        # No textbox for filter string if it's a Reset filter
        if field != "Reset all of the filters applied so far (if any)!":
            el.grid(row=0, column=1)

        def callback_wrapper(input_string: str) -> None:
            """ A wrapper to call the callback function on the <input_string>
            and print the time taken for the function to execute.
            """
            nonlocal new_drawables
            nonlocal m
            t1 = time.time()
            new_drawables = callback(customers, drawables, input_string.upper())
            t2 = time.time()
            print("Time elapsed:  " + str(t2 - t1))
            m.destroy()

        Button(m, text="Apply Filter",
               command=lambda:
               callback_wrapper(el.get()
                                if field != "Reset all of the filters applied "
                                            "so far (if any)!"
                                else "")).grid(row=1, column=0,
                                               sticky=W, pady=5)
        m.mainloop()
        print("FILTER APPLIED")
        return new_drawables

    def display_summary(self, customers: List[Customer]) -> None:
        """ Prompts user for a reservation ID, displays that trip's Summary. """
        m = Tk()
        m.title("Trip Summary")
        Label(m, text="Enter a Reservation ID").grid(row=0)
        el = Entry(m)
        el.grid(row=0, column=1)
        
        def pretty_print(input_string: str, all_customers: List[Customer]
                         ) -> None:
            """ Finds the correct Trip, corresponding to the <input_string>, 
                and aids in the 'pretty' display of its summary.
            """
            nonlocal m
            exists = False
            if all_customers:
                for cus in all_customers:
                    for tp in cus.get_trips():
                        if tp.get_reservation_id() == input_string:
                            exists = True
                            print("-------------------------------------------")
                            print("Summary of Trip (ID: {}):".
                                  format(input_string))
                            print("-------------------------------------------")
                            print("The itinerary for this trip is: {}.".
                                  format(tp.get_flight_segments()))
                            print("The cost of this trip is: ${:.2f}.".
                                  format(cus.get_cost_of_trip(tp)))
                            print("The total trip time is: {}-minutes.".
                                  format(tp.get_total_trip_time()))
                            print("The time in-flight is: {}-minutes.".
                                  format(tp.get_in_flight_time()))
                            print("-------------------------------------------")
                            print("\n")
                if not exists:
                    print("This Trip (ID: {}) does not exist in your dataset!"
                          .format(input_string))
            else:
                print("There are no Trips in your dataset!")
            
            m.destroy()
        
        Button(m, text="Print Summary",
               command=lambda: pretty_print(el.get().upper(), customers))\
            .grid(row=1, column=0, sticky=W, pady=5)

        m.mainloop()


class Map:
    """ Window panning and zooming interface.

    === Public attributes ===
    image:
        the full image for the area to cover with the map
    min_coords:
        the minimum long/lat coordinates
    max_coords:
        the maximum long/lat coordinates
    screensize:
        the dimensions of the screen
    """
    # === Private attributes ===
    # _x_offset:
    #    offset on x axis
    # _y_offset:
    #    offset on y axis
    # _zoom:
    #    map zoom level
    image: pygame.image
    min_coords: Tuple[float, float]
    max_coords: Tuple[float, float]
    screensize: Tuple[int, int]
    _x_offset: int
    _y_offset: int
    _zoom: int

    def __init__(self, screen_dims: Tuple[int, int]) -> None:
        """ Initialize this map for the screen dimensions <screen_dims>. """
        self.image = pygame.image.load(
            os.path.join(os.path.dirname(__file__), MAP_FILE))
        self.min_coords = MAP_MIN
        self.max_coords = MAP_MAX
        self._x_offset = 0
        self._y_offset = 0
        self._zoom = 1
        self.screensize = screen_dims

    def render_objects(self, drawables: List[FlightSegment],
                       screen: pygame.Surface) -> None:
        """ Render the <drawables> onto the <screen>. """
        for drw in drawables:
            long_lat_position = drw.get_long_lat()
            pygame.draw.aaline(screen, LINE_COLOUR,
                               self._long_lat_to_screen(long_lat_position[0]),
                               self._long_lat_to_screen(long_lat_position[1]))

    def _long_lat_to_screen(self, location: Tuple[float, float]) \
            -> Tuple[int, int]:
        """ Convert the <location> longitude/latitude coordinates into pixel
            coordinates.
        """
        x = round((location[0] - self.min_coords[0]) /
                  (self.max_coords[0] - self.min_coords[0]) *
                  self.image.get_width())
        y = round((location[1] - self.min_coords[1]) /
                  (self.max_coords[1] - self.min_coords[1]) *
                  self.image.get_height())

        x = round((x - self._x_offset) * self._zoom * self.screensize[0] /
                  self.image.get_width())
        y = round((y - self._y_offset) * self._zoom * self.screensize[1] /
                  self.image.get_height())

        return x, y

    def pan(self, dp: Tuple[int, int]) -> None:
        """ Pan the view in the image by <dp> (dx, dy) screenspace pixels. """
        self._x_offset -= dp[0]
        self._y_offset -= dp[1]
        self._clamp_transformation()

    def zoom(self, dx: float) -> None:
        """ Zoom the view by <dx> amount.

            The centre of the zoom is the top-left corner of the visible region.
        """
        if (self._zoom >= 4 and dx > 0) or (self._zoom <= 1 and dx < 0):
            return

        self._zoom += dx
        self._clamp_transformation()

    def _clamp_transformation(self) -> None:
        """ Ensure that the transformation parameters are within a fixed range.
        """
        raw_width = self.image.get_width()
        raw_height = self.image.get_height()
        zoom_width = round(raw_width / self._zoom)
        zoom_height = round(raw_height / self._zoom)

        self._x_offset = min(raw_width - zoom_width, max(0, self._x_offset))
        self._y_offset = min(raw_height - zoom_height, max(0, self._y_offset))

    def get_current_view(self) -> pygame.Surface:
        """ Get the sub-image to display to screen from the map. """
        raw_width = self.image.get_width()
        raw_height = self.image.get_height()
        zoom_width = round(raw_width / self._zoom)
        zoom_height = round(raw_height / self._zoom)

        map_segment = self.image.subsurface(((self._x_offset, self._y_offset),
                                             (zoom_width, zoom_height)))
        return pygame.transform.smoothscale(map_segment, self.screensize)


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': [
            'doctest', 'python_ta', 'typing',
            'tkinter', 'os', 'pygame',
            'threading', 'math', 'time',
            'customer', 'flight', 'filter', 'typing'
        ],
        'allowed-io': [
            'entry_window', 'callback_wrapper', 'threading_wrapper',
            '__init__', 'handle_window_events', 'display_summary',
            'pretty_print'
        ],
        'disable': ['R0915', 'W0401', 'R0201'],
        'generated-members': 'pygame.*',
        'max-args': 6,
        'max-nested-blocks': 4
    })
