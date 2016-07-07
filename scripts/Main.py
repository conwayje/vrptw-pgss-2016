from Customer import Customer
from Truck import Truck
from Depot import Depot
from Cluster import Cluster
from Visual import Visual
from Path import Path
from ImportCustomers import import_customers

def init():
    customers = import_customers("C201.txt")
    #cusomers = import_customers("RC208.txt")
    depot = Depot()
    truck1 = Truck(1, 0, 0, 700)
    truck2 = Truck(2,0,0,700)
    truck3 = Truck(3,0,0,700)
    Visual.plot_customers(depot, customers)
    
init()