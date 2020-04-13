""" Supermarket simulation
This module reads the probability tables and arrays processed by
probability_matrix_and_array.py to simulate customer behavior.
"""

import numpy as np
import random
from random import randint
import cv2
from probability_matrix_and_array import PorbabilityClass


class Customer(PorbabilityClass):
    """
    This is the Customer class inheriting ProbabilityClass as the parent class to
    use probability matrix and arrays for simulating customers.
    """

    def __init__(self, weekday, aisle='fruit'):
        """
        Parameters
        ----------
        aisle: str
            name of the aisle in the supermarket
        weekday: str
            either a day of the week from Monday to Friday or all_days
        image: np.array
            a black square representing the customer's image
        location: np.array
            entrace location in the supermarket and the starting position of the customers
        h: int
            hight of image
        w: int
            width of image
        payment: float
            the amount of money the custmer has spent
        aisles_locs: dict
            coordinates of the aisles
        revenue_min: dict
            revenue per minutes of each aisle
        money_per_aisle: dict
            money spent at each aisle by the customer
        """
        super().__init__(aisle, weekday)
        image = np.zeros((10, 10, 3), dtype=np.uint8)
        image[:, :] = 0
        self.image = image
        self.location = np.array((randint(600, 660), randint(750, 880)))
        self.h = self.image.shape[0]
        self.w = self.image.shape[1]
        self.payment = 0
        self.shopping_hist = []
        self.aisles_locs = {
                            'fruit': np.array((randint(160, 400), randint(760, 790))),
                            'spices': np.array((randint(160, 400), randint(570, 630))),
                            'drinks': np.array((randint(160, 400), randint(140, 180))),
                            'dairy': np.array((randint(160, 400), randint(335, 360))),
                            'checkout': (600, randint(70, 100))
                            }
        self.revenue_min = {'fruit': 4, 'spices': 3, 'drinks': 6, 'dairy': 5, 'checkout': 0}
        self.money_per_aisle = {'fruit': 0, 'spices': 0, 'drinks': 0, 'dairy': 0, 'checkout': 0}

    def aisle_pattern(self):
        """
        Generates the first aisle the customer visits and the following ones
        using first aisle probability array and probability matrix (Markov chain)
        from porb_matrix_by_day method.
        """
        # place the customer in the 'first_aisle - every aisle except checkout'
        initial_state, prob_mat = self.porb_matrix_by_day()
        aisle = random.choices(initial_state.index, initial_state)[0]
        yield aisle
        # for every other time until she checkouts, place her wherever the aisle_activity prob matrix places her
        while True:
            aisle = random.choices(prob_mat.index, prob_mat.loc[aisle])[0]
            yield aisle

    def det_target(self):
        """
        Set the target location as the start location after the customer reaches
        to the aisle and has to go to the next aisle
        """
        if self.location[0] == self.target_position[0] and self.location[1] == self.target_position[1]:
            if self.target_position[0] != 600 and self.target_position[1] != 220:
                self.target_position = np.array(self.aisles_locs[self.target_list[1]])
                self.target_list.pop(1)

    def move(self):
        '''
        This method moves the customers in the supermarket
        based on the initial location and the target_position.
        '''

        y, x = self.location
        ty, tx = self.target_position
        edge = 60
        # go up
        if x != tx and y != edge:
            trajectory = edge - y
            if trajectory > 0:
                self.location[0] += 1
            elif trajectory < 0:
                self.location[0] -= 1

        # go right or left
        if x != tx and y == edge:
            trajectory = tx - x
            if trajectory > 0:
                self.location[1] += 1
            if trajectory < 0:
                self.location[1] -= 1

        # go down
        if x == tx:
            trajectory = ty - y
            if trajectory > 0:
                self.location[0] += 1
            if trajectory < 0:
                self.location[0] -= 1

    def money_spent(self):
        """
        Calculates the amount of money customers spent at each aisle
        based on the the time they spent at it.

        Takes the sector_time_prob  array to simulate the minutes spent and mutiply it by the
        revenue per minutes provided before in the revenue_min dictionary
        """
        for aisle in self.shopping_hist:
            self.aisle = aisle
            time_prob = self.sector_time_prob()
            time_spent = random.choices(time_prob.index, time_prob)[0]
            pay = self.revenue_min[aisle] * time_spent
            self.payment = self.payment + pay
            self.money_per_aisle[aisle] = pay


    def pattern(self):
        """
        Simulate the shopping pattern by using the aisle_pattern method.

        Appending the name of the each visited aisle to the shopping history
        list and finally stops the pattern when it reaches to the checkout section.
        """
        pattern_func = self.aisle_pattern()
        while True:
            next_step = next(pattern_func)
            self.shopping_hist.append(next_step)
            if next_step == 'checkout':
                break
        self.target_list = self.shopping_hist.copy()
        self.target_position = np.array(self.aisles_locs[self.shopping_hist[0]])

class SupermarketSim(Customer):
    """
    The SupermarketSim class is a child class of Customer class and it
    visualizes the movement of the customers in the supermarket based on their
    shopping_hist from Customer class
    """

    def __init__(self, customers, background=cv2.imread('..\\data\\market.png')):
        """
        Parameters
        ----------
        customers: list
            list of customers simulated by Customer class with defined moement pattern and payment
        background: png
            supermarket image
        """
        image: np.array
        self.background = background
        self.customers = customers
        self.frame = background

    def draw(self):
        """
        Places the customers symbol image on the supermarket image based on they
        customer.location coordinates and the size of the symbol.
        """
        self.frame = self.background.copy()
        for customer in self.customers:
            y, x = customer.location
            self.frame[y:y+customer.h, x:x+customer.w] = customer.image

    def run_one_iteration(self):
        """
        Moves each customer from starting position and the target position using
        move and det_target methods from Customer class.
        """
        for customer in self.customers:
            customer.move()
            customer.det_target()
