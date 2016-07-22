"""	Returns a State for a supplied solution
"""

from ImportCustomers import import_customers
from Depot import Depot
from Path import Path
from Truck import Truck
from State import State
from Distances import Distances

from Visual import Visual
import argparse

path = '../standard_instances/'

def import_solution(filename):
    with open(path + filename) as f:
        customers = import_customers(filename.split("_")[0] + ".txt")
        lines = f.readlines()

        ids = []
        # @TODO -- truck number dependency (from here until the end of the function)
        ids.append(lines[5].split()[3:])
        ids.append(lines[6].split()[3:])
        ids.append(lines[7].split()[3:])


    routes = []
    for line in ids:
        route = []
        for cust_number in line:
            route.append((customers[int(cust_number)-1]))
        routes.append(route)


    trucks = []
    for i in range(len(routes)):
        trucks.append(Truck(i, 0, 0, truck_capacity, Path(routes[i])))

    return State(trucks)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()
    filename = args.filename

    state = import_solution(filename)

    # plot solution
    # state.plot()

    # plot missed customers
    # state.plot_missed()

    # print number of missed customers
    # print len(state.truck1.path.is_valid()) + len(state.truck2.path.is_valid()) + len(state.truck3.path.is_valid())