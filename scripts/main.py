""" This is the main py file to run the simulation.

It accepts two outputs:
 1. Day of the week that the user wants the simulation to run on
 2. Number of the customers

A new window will open and a visualization of the simulation will show the
customers shopping pattern and the amount of money they spend at each section
based on the time they spend at the aisle.
 """

from supermarket_sim import SupermarketSim, Customer
import numpy as np
import cv2


if __name__ == '__main__':

    print("Please enter a day of the week from Monday to Friday or write 'all_days'for the whole week:\n")
    WEEKDAY = input()
    print("\nPlease enter the number of customers to simulate:\n")
    NUMBER = input()

    # simulating the given number of customers using Customer class
    CUSTOMERS = []
    for _ in range(int(NUMBER)):
        C = Customer(weekday=(f'{WEEKDAY}'))
        C.pattern()
        C.money_spent()
        CUSTOMERS.append(C)

    for CUSTOMER in CUSTOMERS:
        print(CUSTOMER.shopping_hist)
        print(CUSTOMER.payment)
        # print(customer.money_per_aisle)

    SIM = SupermarketSim(CUSTOMERS)
    IMG = cv2.imread('..\\data\\market.png')

    AISLE_INCOME = {
                    'fruit': [0, (780, 130)],
                    'spices': [0, (560, 130)],
                    'drinks': [0, (100, 130)],
                    'dairy': [0, (330, 130)],
                    'checkout': [0, (480, 650)]
                    }
    while True:

        FRAME = IMG.copy()
        LAYER = np.zeros((SIM.frame.shape[0], SIM.frame.shape[1], 3))
        SIM.draw()
        SIM.run_one_iteration()

        # calculating the total income of the supermarket based on the simulation
        for CUSTOMER in SIM.customers:
            if CUSTOMER.location[0] == CUSTOMER.target_position[0] and CUSTOMER.location[1] == CUSTOMER.target_position[1]:
                AISLE_INCOME['checkout'][0] += CUSTOMER.payment
                SIM.customers.remove(CUSTOMER)

        # calculating the total income of each aisle
        for CUSTOMER in SIM.customers:
            for KEY in AISLE_INCOME.keys():
                if CUSTOMER.location[0] == CUSTOMER.aisles_locs[KEY][0] and CUSTOMER.location[1] == CUSTOMER.aisles_locs[KEY][1]:
                    AISLE_INCOME[KEY][0] += CUSTOMER.money_per_aisle[KEY]
                    print(AISLE_INCOME)

        # visualizing the payed amount at each aisle
        for AISLE in AISLE_INCOME.keys():
            cv2.putText(LAYER, f"{int(AISLE_INCOME[AISLE][0])}", AISLE_INCOME[AISLE][1], cv2.FONT_HERSHEY_SIMPLEX, 1, (1, 1, 1), 2)


        cnd = LAYER[:] > 0
        SIM.frame[cnd] = LAYER[cnd]

        cv2.imshow('frame', SIM.frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
