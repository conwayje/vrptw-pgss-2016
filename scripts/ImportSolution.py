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

def import_solution(problem, filename):
    with open(path + filename) as f:
        customers = import_customers(problem, False)
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

def write_solution(state, filename):
    with open(path + filename + ".txt", 'w') as f:
        for x in range(5):
            f.write('\n')
        for x in range(len(state.trucks)):
            line = "Route {0} : ".format(x + 1)
            for customer in state.trucks[x].path.route:
                line += str(customer.number)
                line += " "
            f.write(line + "\n")


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