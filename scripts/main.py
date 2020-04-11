from supermarket_sim import SupermarketSim, Customer
import numpy as np
import cv2
from config import PATH



if __name__=='__main__':

    customers = []
    for _ in range(5):
        c = Customer(weekday='Friday', image=cv2.imread(f'{PATH}customer_2.png'))
        c.pattern()
        c.money_spent()
        customers.append(c)

    for customer in customers:
        print(customer.shopping_hist)
        print(customer.payment)

    sim = SupermarketSim(customers)
    img = cv2.imread(f'{PATH}market.png')

    income = []
    while True:

        frame = img.copy()
        layer = np.zeros((sim.frame.shape[0], sim.frame.shape[1], 3))
        sim.draw()
        sim.run_one_iteration()

        for customer in sim.customers:
            if customer.location[0] == customer.target_position[0] and customer.location[1] == customer.target_position[1]:
                income.append(customer.payment)
                sim.customers.remove(customer)

        cv2.putText(layer, f'{int(sum(income))}', (10, 500), cv2.FONT_HERSHEY_SIMPLEX, 1, (1, 1, 1), 2)

        cnd = layer[:] > 0
        sim.frame[cnd] = layer[cnd]

        cv2.imshow('frame', sim.frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    cv2.destroyAllWindows()
