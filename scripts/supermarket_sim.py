import numpy as np
import random
from random import randint
import cv2
from probability_matrix_and_array import PorbabilityClass


class Customer(PorbabilityClass):
    """ This is a customer class """

    def __init__(self, aisle, weekday, image):
        PorbabilityClass.__init__(self, aisle, weekday)
        self.image = image
        self.location = np.array((randint(600, 620), randint(730, 790)))
        self.h = self.image.shape[0]
        self.w = self.image.shape[1]
        self.payment = 0
        self.shopping_hist = []
        self.aisles_locs = {'fruit': (180, 750), 'spices': (150, 570), 'drinks': (280, 140), 'dairy': (130, 335), 'checkout': (600, 80)}

    def aisle_pattern(self):
        # first time your customer arrives, place her in the 'first_aisle - every aisle except checkout'
        initial_state, prob_mat = self.porb_matrix_by_day()
        aisle = random.choices(initial_state.index, initial_state)[0]
        yield aisle
        # for every other time until she checkouts, place her wherever the aisle_activity prob matrix places her
        while True:
            aisle = random.choices(prob_mat.index, prob_mat.loc[aisle])[0]
            yield aisle

    def det_target(self):
        if self.location[0] == self.target_position[0] and self.location[1] == self.target_position[1]:
            if self.target_position[0] != 600 and self.target_position[1] != 220:
                self.target_position = np.array(self.aisles_locs[self.target_list[1]])
                self.target_list.pop(1)

    def move(self):
        '''
        The method move lets the customers move in the supermarket
        '''

#         for i in range(len(self.shopping_hist)):
        y, x = self.location
        ty, tx = self.target_position

        # go up
        if x != tx and y != 60:
            trajectory = 60 - y
            if trajectory > 0:
                self.location[0] += 1
            elif trajectory < 0:
                self.location[0] -= 1

        # go right or left
        if x != tx and y == 60:
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


    def money_spent(self):  # make this code better Amirali!!!
        for section in self.shopping_hist:
            if section == 'dairy':
                self.aisle = 'dairy'
                time_prob = self.sector_time_prob()
                time_spent = random.choices(time_prob.index, time_prob)[0]
                pay = 5 * time_spent
                self.payment = self.payment + pay
            if section == 'fruit':
                self.aisle = 'fruit'
                time_prob = self.sector_time_prob()
                time_spent = random.choices(time_prob.index, time_prob)[0]
                pay = 4 * time_spent
                self.payment = self.payment + pay
            if section == 'spices':
                self.aisle = 'spices'
                time_prob = self.sector_time_prob()
                time_spent = random.choices(time_prob.index, time_prob)[0]
                pay = 3 * time_spent
                self.payment = self.payment + pay
            if section == 'drinks':
                self.aisle = 'drinks'
                time_prob = self.sector_time_prob()
                time_spent = random.choices(time_prob.index, time_prob)[0]
                pay = 6 * time_spent
                self.payment = self.payment + pay
            else:
                self.payment = self.payment

    def pattern(self):
        pattern_func = self.aisle_pattern()
        while True:
            next_step = next(pattern_func)
            self.shopping_hist.append(next_step)
            if next_step == 'checkout':
                break
        self.target_list = self.shopping_hist.copy()
        self.target_position = np.array(self.aisles_locs[self.shopping_hist[0]])

class SupermarketSim(Customer):

    def __init__(self, customers, background=cv2.imread('market.png')):
        self.background = background
        self.customers = customers
        self.frame = background

    def draw(self):
        self.frame = self.background.copy()
        for customer in self.customers:
            y, x = customer.location
            self.frame[y:y+customer.h, x:x+customer.w] = customer.image

    def run_one_iteration(self):
        for customer in self.customers:
            customer.move()
            customer.det_target()