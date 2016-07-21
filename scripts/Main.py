from Customer import Customer
from Truck import Truck
from Depot import Depot
from Cluster import Cluster
from Visual import Visual
from Path import Path
from State import State
from AStar import doAStar
from ImportCustomers import import_customers
from ImportSolution import import_solution
from Distances import Distances
from Dijkstra import get_nearest_neighbors_all_trucks
import copy
import argparse

# Filenames:    C201.txt, C201_wr_solution.txt
# 				RC208.txt, RC208_wr_solution.txt

customers = None
depot = None

# @TODO -- Truck number dependency
truck1 = None
truck2 = None
truck3 = None

def init(filename):
    global customers, depot, truck1, truck2, truck3

    customers = import_customers(filename)
    Distances.calculate_matrix(customers)
    depot = Depot(0,0)

    # @TODO -- truck number dependency
    truck1 = Truck(1,0,0,700)
    truck2 = Truck(2,0,0,700)
    truck3 = Truck(3,0,0,700)

    # plot the problem
    # Visual.plot_customers(depot, customers)
    # Visual.show()

def initial_state(filename):
    global customers, depot, truck1, truck2, truck3

    # @TODO -- truck number dependency
    route1 = []
    route2 = []
    route3 = []

    # @TODO -- this seems a little bit more naive than we want for an initial solution =/
    # maybe try to do something along these lines but also implement dijkstra or something like that?
    # as in:  partition into three sets, and then for each set, go to the closest remaining unserved customer
    # until there are no customers remaining.
    # just a suggestion; y'all can be as creative as you want

    state = import_solution(filename)
    state.plot()


    # depot_c = Customer(0, 0, 0, 0, 0, 0, 0)  # @HACK
    # c = [depot_c]
    # for cust in customers:
    #     c.append(cust)
    # return get_nearest_neighbors_all_trucks(c, depot_c, 3)

    return state

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("problem_file")
    parser.add_argument("init_solution_file")
    args = parser.parse_args()
    problem_file = args.problem_file + ".txt"
    init_solution_file = args.init_solution_file + ".txt"

    init(problem_file)
    doAStar(initial_state(init_solution_file))