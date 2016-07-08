from Customer import Customer
from Truck import Truck
from Depot import Depot
from Cluster import Cluster
from Visual import Visual
from Path import Path
from State import State
from ImportCustomers import import_customers

truck1 = None
truck2 = None
truck3 = None
customers = None

def init():
    global customers, depot, truck1, truck2, truck3
    customers = import_customers("C201.txt")
    #cusomers = import_customers("RC208.txt")
    depot = Depot()
    truck1 = Truck(1, 0, 0, 700)
    truck2 = Truck(2,0,0,700)
    truck3 = Truck(3,0,0,700)
    #Visual.plot_customers(depot, customers)

def initial_state():
    global customers, truck1, truck2, truck3
    route1 = []
    route2 = []
    route3 = []
    for customer in customers:
        if customer.x < 0 and customer.y > -15:
            route1.append(customer)
        elif customer.x >= 0 and customer.y > -15:
            route2.append(customer)
        else:
            route3.append(customer)
    truck1.path = Path(route1)
    truck2.path = Path(route2)
    truck3.path = Path(route3)

    state = State(truck1, truck2, truck3)
    print truck1.path.is_valid()
    print truck2.path.is_valid()
    print truck3.path.is_valid()
    state.plot()
    return state

init()
initial_state()