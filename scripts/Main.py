from Customer import Customer
from Truck import Truck
from Depot import Depot
from Cluster import Cluster
from Visual import Visual
from Path import Path
from State import State
from AStar import doAStar
from ImportCustomers import import_customers
#from ImportSolution import import_solution

# Filenames:    C201.txt, C201_wr_solution.txt
# 				RC208.txt, RC208_wr_solution.txt

truck1 = None
truck2 = None
truck3 = None
customers = None
depot = Depot()

def init():
    global customers, depot, truck1, truck2, truck3

    # @TODO -- let's replace this with argument parsing >.>
    # otherwise we're editing source all the time, which is lame
    # there's an example in ImportSolution.py
    customers = import_customers("C201.txt")

    depot = Depot()
    truck1 = Truck(1, 0, 0, 700)
    truck2 = Truck(2,0,0,700)
    truck3 = Truck(3,0,0,700)

    # Visual.plot_customers(depot, customers)

def initial_state():
    global customers, truck1, truck2, truck3
    route1 = []
    route2 = []
    route3 = []

    customers_by_distance = sorted(customers, key=lambda customer: customer.distance()*customer.timewindow())
    # customers_by_distance = customers.closest_customers()

    # print customers_by_distance

    # @TODO -- this seems a little bit more naive than we want for an initial solution =/
    # maybe try to do something along these lines but also implement dijkstra or something like that?
    # as in:  partition into three sets, and then for each set, go to the closest remaining unserved customer
    # until there are no customers remaining.
    # just a suggestion; y'all can be as creative as you want
    for customer in customers_by_distance:
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


    #state = import_solution("C201_wr_solution.txt")
    state.plot()

    return state

init()
i_state = initial_state()

#solution_file = "../standard_instances/Jahnik"
#
## @TODO we should probably not put this in main?
#f = file(solution_file, "r")
#solution_lines = f.readlines()
#f.close()
#
#truck_1_path = solution_lines[0].strip()
#truck_2_path = solution_lines[1].strip()
#truck_3_path = solution_lines[2].strip()
#
#
#route1 = []
#route2 = []
#route3 = []
#
#for i in truck_1_path.split(' '):
#    print i,
#    route1.append(customers[int(i)-1])
#
#print "\n"
#for i in truck_2_path.split(' '):
#    print i,
#    route2.append(customers[int(i)-1])
#
#print "\n"
#for i in truck_3_path.split(' '):
#    print i,
#    route3.append(customers[int(i)-1])
#
#
#
#i_state = State(Truck(1, 0, 0, 700, Path(route1)), Truck(2, 0, 0, 700, Path(route2)) ,Truck(3, 0, 0, 700, Path(route3)))
#
#
#i_state.plot()
#
#paths = [i_state.truck1.path, i_state.truck2.path, i_state.truck3.path]
#for path in paths:
#    for cust in path.route:
#        print path.route.index(cust), cust, path.get_arrival_time_of_customer(cust)

paths = [i_state.truck1.path, i_state.truck2.path, i_state.truck3.path]
# for path in paths:
#     for cust in path.route:
#         print path.route.index(cust), cust, path.get_arrival_time_of_customer(cust)

doAStar(i_state)




