from supermarket_sim import SupermarketSim, Customer
import numpy as np
import cv2
from config import PATH


if __name__ == '__main__':

    CUSTOMERS = []
    for _ in range(5):
        C = Customer(weekday='Friday')
        C.pattern()
        C.money_spent()
        CUSTOMERS.append(C)

    for customer in CUSTOMERS:
        print(customer.shopping_hist)
        print(customer.payment)
        # print(customer.money_per_aisle)

    SIM = SupermarketSim(CUSTOMERS)
    IMG = cv2.imread(f'{PATH}market.png')

    AISLE_INCOME = {'fruit': 0, 'spices': 0, 'drinks': 0, 'dairy': 0}
    INCOME = []
    while True:

        frame = IMG.copy()
        layer = np.zeros((SIM.frame.shape[0], SIM.frame.shape[1], 3))
        SIM.draw()
        SIM.run_one_iteration()

        for customer in SIM.customers:
            if customer.location[0] == customer.target_position[0] and customer.location[1] == customer.target_position[1]:
                INCOME.append(customer.payment)
                SIM.customers.remove(customer)

        for customer in SIM.customers:
            for key in AISLE_INCOME.keys():
                if customer.location[0] == customer.aisles_locs[key][0] and customer.location[1] == customer.aisles_locs[key][1]:
                    AISLE_INCOME[key] += customer.money_per_aisle[key]
                    print(AISLE_INCOME)



        cv2.putText(layer, f"{int(AISLE_INCOME['fruit'])}", (650, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (1, 1, 1), 2)
        cv2.putText(layer, f"{int(AISLE_INCOME['spices'])}", (450, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (1, 1, 1), 2)
        cv2.putText(layer, f"{int(AISLE_INCOME['drinks'])}", (350, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (1, 1, 1), 2)
        cv2.putText(layer, f"{int(AISLE_INCOME['dairy'])}", (200, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (1, 1, 1), 2)

        cv2.putText(layer, f'{int(sum(INCOME))}', (10, 500), cv2.FONT_HERSHEY_SIMPLEX, 1, (1, 1, 1), 2)

        cnd = layer[:] > 0
        SIM.frame[cnd] = layer[cnd]

        cv2.imshow('frame', SIM.frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    cv2.destroyAllWindows()
