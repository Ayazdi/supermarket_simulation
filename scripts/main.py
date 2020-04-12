from supermarket_sim import SupermarketSim, Customer
import numpy as np
import cv2
from config import PATH


if __name__ == '__main__':

    print("Please enter a day of the week from Monday to Friday or write 'all_days'for the whole week:\n")
    WEEKDAY = input()
    print("\nPlease enter the number of customers to simulate:\n")
    NUMBER = input()

    CUSTOMERS = []
    for _ in range(int(NUMBER)):
        C = Customer(weekday=str(WEEKDAY))
        C.pattern()
        C.money_spent()
        CUSTOMERS.append(C)

    for CUSTOMER in CUSTOMERS:
        print(CUSTOMER.shopping_hist)
        print(CUSTOMER.payment)
        # print(customer.money_per_aisle)

    SIM = SupermarketSim(CUSTOMERS)
    IMG = cv2.imread(f'{PATH}market.png')

    AISLE_INCOME = {'fruit': 0, 'spices': 0, 'drinks': 0, 'dairy': 0}
    INCOME = []
    while True:

        FRAME = IMG.copy()
        LAYER = np.zeros((SIM.frame.shape[0], SIM.frame.shape[1], 3))
        SIM.draw()
        SIM.run_one_iteration()

        for CUSTOMER in SIM.customers:
            if CUSTOMER.location[0] == CUSTOMER.target_position[0] and CUSTOMER.location[1] == CUSTOMER.target_position[1]:
                INCOME.append(CUSTOMER.payment)
                SIM.customers.remove(CUSTOMER)

        for CUSTOMER in SIM.customers:
            for KEY in AISLE_INCOME.keys():
                if CUSTOMER.location[0] == CUSTOMER.aisles_locs[KEY][0] and CUSTOMER.location[1] == CUSTOMER.aisles_locs[KEY][1]:
                    AISLE_INCOME[KEY] += CUSTOMER.money_per_aisle[KEY]
                    print(AISLE_INCOME)

        # payed amount at each aisle
        cv2.putText(LAYER, f"{int(AISLE_INCOME['fruit'])}", (820, 130), cv2.FONT_HERSHEY_SIMPLEX, 1, (1, 1, 1), 2)
        cv2.putText(LAYER, f"{int(AISLE_INCOME['spices'])}", (580, 130), cv2.FONT_HERSHEY_SIMPLEX, 1, (1, 1, 1), 2)
        cv2.putText(LAYER, f"{int(AISLE_INCOME['dairy'])}", (330, 130), cv2.FONT_HERSHEY_SIMPLEX, 1, (1, 1, 1), 2)
        cv2.putText(LAYER, f"{int(AISLE_INCOME['drinks'])}", (100, 130), cv2.FONT_HERSHEY_SIMPLEX, 1, (1, 1, 1), 2)
        # total income
        cv2.putText(LAYER, f'{int(sum(INCOME))}', (10, 500), cv2.FONT_HERSHEY_SIMPLEX, 1, (1, 1, 1), 2)

        cnd = LAYER[:] > 0
        SIM.frame[cnd] = LAYER[cnd]

        cv2.imshow('frame', SIM.frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    cv2.destroyAllWindows()
