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
        customers = import_customers(filename.split("_")[0] + ".txt", False)
        lines = f.readlines()

        ids = []
        for line in lines[5:]:
            ids.append(line.split()[3:])

    routes = []
    for line in ids:
        route = []
        for cust_number in line:
            route.append((customers[int(cust_number)-1]))
        routes.append(route)

    trucks = []
    for i in range(len(routes)):
        trucks.append(Truck(i, 0, 0, len(routes), Path(routes[i])))

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