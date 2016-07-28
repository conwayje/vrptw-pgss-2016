from Customer import Customer
from Truck import Truck
from Depot import Depot
from Cluster import Cluster
from Visual import Visual
from Path import Path
from State import State
from AStar import doAStar
from ImportCustomers import import_customers
from ImportSolution import *
from Distances import Distances
from Dijkstra import Dijsktra
from ClusterStore import ClusterStore
import datetime
import copy
import argparse
# Filenames:    C201.txt, C201_wr_solution.txt
#               RC208.txt, RC208_wr_solution.txt

# sample calls (made from inside the scripts directory):
# python Main.py C201 C201_wr_solution 3 700 591.56 --plot
# python Main.py C202 nn_random 3 700 591.56 --plot
# python Main.py RC208 RC208_wr_solution 3 1000 828.15 --plot

customers = None
depot = None
num_trucks = None
truck_capacity = None

def init(filename):
    global customers, depot

    print "Importing customers..."
    customers = import_customers(filename + ".txt", test_environment )
    print "Calculating distances..."
    Distances.calculate_matrix(customers)
    print "Storing clusters..."
    ClusterStore.store_clusters(filename, customers)

    depot = Depot(0,0)

def initial_state(problem, filename):
    global customers

    if filename == "nearest_neighbors":
        print "Generating nearest neighbors solution..."
        depot_c = Customer(0, 0, 0, 0, 0, 0, 0)
        c = [depot_c]
        for cust in customers:
            c.append(cust)

        paths = Dijsktra.get_nearest_neighbors_all_trucks(c, depot_c, num_trucks)

        trucks = []
        for k in range(1, num_trucks + 1):
            t = Truck(k, 0, 0, truck_capacity, path = Path(paths[k-1][1:]))
            trucks.append(t)

        state = State( trucks, parent = None )
    
    elif filename == "nn_random":
        print "Generating nearest neighbors random solution..."
        depot_c = Customer(0, 0, 0, 0, 0, 0, 0)
        c = [depot_c]
        for cust in customers:
            c.append(cust)

        paths = Dijsktra.get_nearest_neighbors_random(c, depot_c, num_trucks, 2)

        trucks = []
        for k in range(1, num_trucks + 1):
            t = Truck(k, 0, 0, truck_capacity, path = Path(paths[k-1][1:]))
            trucks.append(t)

        state = State( trucks, parent = None )
        state.plot()

    else:
        state = import_solution(problem, filename)

    if do_plot:
        state.plot()

    return state

parser = argparse.ArgumentParser()
parser.add_argument("problem_file")
parser.add_argument("init_solution_file")
parser.add_argument("num_trucks")
parser.add_argument("truck_capacity")
parser.add_argument("world_record_score")
parser.add_argument("--plot", help="plot the map before the main loop engages", action = "store_true")
parser.add_argument("--test", help="looks into the test directory rather than main directory", action = "store_true")
args = parser.parse_args()
problem_file = args.problem_file
init_solution_file = args.init_solution_file
num_trucks = int(args.num_trucks)
do_plot = args.plot
truck_capacity = int(args.truck_capacity)
world_record_score = float( args.world_record_score )
test_environment = args.test

init(problem_file)
state = doAStar(initial_state(problem_file, init_solution_file), do_plot, world_record_score)

states = []
while state.parent != None:
    # raw_input("\nEnter to see parent")
    # state.plot()
    states.append(state)
    state = state.parent
filename = "solution_path_" + datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
write_solution_path(states, filename)
