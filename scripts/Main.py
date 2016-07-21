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
from Dijkstra import Dijsktra
import copy
import argparse

# Filenames:    C201.txt, C201_wr_solution.txt
# 				RC208.txt, RC208_wr_solution.txt

customers = None
depot = None
num_trucks = 0


def init(filename):
    global customers, depot

    customers = import_customers(filename + ".txt")
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

    # @TODO -- just for testing, write init solutions to file
    if filename == "nearest_neighbors":
        depot_c = Customer(0, 0, 0, 0, 0, 0, 0)
        c = [depot_c]
        for cust in customers:
            c.append(cust)
            
        paths = Dijsktra.get_nearest_neighbors_all_trucks(c, depot_c, 3)
        state = State([Truck(1, 0, 0, 700, path=Path(paths[0][1:])),
                      Truck(2, 0, 0, 700, path=Path(paths[1][1:])),
                      Truck(3, 0, 0, 700, path=Path(paths[2][1:]))], parent=None)
        
        if do_plots:
            state.plot()

    else:
        state = import_solution(filename  + ".txt")
        if args.plot:
            state.plot()

    return state

parser = argparse.ArgumentParser()
parser.add_argument("problem_file")
parser.add_argument("init_solution_file")
parser.add_argument("num_trucks")
parser.add_argument("--plot", help="plot the map before the main loop engages", action = "store_true")
args = parser.parse_args()
problem_file = args.problem_file
init_solution_file = args.init_solution_file
num_trucks = args.num_trucks
do_plots = args.plot

init(problem_file)
doAStar(initial_state(init_solution_file))
