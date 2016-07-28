"""	Returns a State for a supplied solution
"""

from ImportCustomers import import_customers
from Depot import Depot
from Path import Path
from Truck import Truck
from State import State
from Distances import Distances
import time

from Visual import Visual
import argparse

path = '../standard_instances/'

def import_solution(problem, filename):
    with open(path + filename) as f:
        customers = import_customers(problem, False)
        Distances.calculate_matrix(customers)
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

def write_solution_path(states, filename):
    with open(path + filename + ".txt", 'w') as f:
        for state in states:
            for x in range(len(state.trucks)):
                line = "Route {0} : ".format(x + 1)
                for customer in state.trucks[x].path.route:
                    line += str(customer.number)
                    line += " "
                f.write(line + "\n")

def animate(problem, filename, num_trucks):
    with open(path + filename + ".txt") as f:
        customers = import_customers(problem + ".txt", False)
        Distances.calculate_matrix(customers)
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

    truck_lists = []
    for i in range(len(routes)):
        if i % num_trucks == 0:
            truck_lists.append([])
        truck_lists[-1].append(Truck(i % num_trucks, 0, 0, len(routes), Path(routes[i])))

    for trucks in truck_lists:
        State(trucks).plot()
        time.sleep(.3)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("problem")
    parser.add_argument("filename")
    parser.add_argument("num_trucks")
    args = parser.parse_args()
    problem = args.problem
    filename = args.filename
    num_trucks = int(args.num_trucks)
    animate(problem, filename, num_trucks)