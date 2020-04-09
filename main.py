from supermarket_sim import SupermarketSim, Customer
import cv2



if __name__=='__main__':

    customers = []
    for _ in range(2):
        c = Customer(weekday='all_days', aisle='fruit', image=cv2.imread('customer_2.png'))
        c.pattern()
        c.money_spent()
        customers.append(c)

    for customer in customers:
        print(customer.shopping_hist)
        print(customer.payment)

    sim = SupermarketSim(customers)
    img = cv2.imread('market.png')

    while True:
        frame = img.copy()

        sim.draw()
        sim.run_one_iteration()
        for customer in sim.customers:
            if customer.location[0] == customer.target_position[0] and customer.location[1] == customer.target_position[1]:
                sim.customers.remove(customer)





        cv2.imshow('frame', sim.frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    cv2.destroyAllWindows()
