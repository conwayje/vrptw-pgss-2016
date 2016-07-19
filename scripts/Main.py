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
import argparse

# Filenames:    C201.txt, C201_wr_solution.txt
# 				RC208.txt, RC208_wr_solution.txt

customers = None
depot = None

# @TODO -- Truck number dependency

def init(filename):
    global customers, depot

    customers = import_customers(filename)
    Distances.calculate_matrix(customers)
    depot = Depot(0,0)

    # plot the problem
    # Visual.plot_customers(depot, customers)
    # Visual.show()

def initial_state(filename):
    global customers

    # @TODO -- this seems a little bit more naive than we want for an initial solution =/
    # maybe try to do something along these lines but also implement dijkstra or something like that?
    # as in:  partition into three sets, and then for each set, go to the closest remaining unserved customer
    # until there are no customers remaining.
    # just a suggestion; y'all can be as creative as you want

    state = import_solution(filename)

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