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
from Dijkstra import do_dijkstra
import argparse

# Filenames:    C201.txt, C201_wr_solution.txt
# 				RC208.txt, RC208_wr_solution.txt

customers = None
depot = None
truck1 = None
truck2 = None
truck3 = None


def init(filename = "C201.txt"):
    global customers, depot, truck1, truck2, truck3

    customers = import_customers(filename)
    depot = Depot(0,0)
    truck1 = Truck(1,0,0,700)
    truck2 = Truck(2,0,0,700)
    truck3 = Truck(3,0,0,700)

    # plot the problem
    # Visual.plot_customers(depot, customers)
    # Visual.show()

def initial_state():
    global customers, depot, truck1, truck2, truck3
    route1 = []
    route2 = []
    route3 = []

    # @TODO -- this seems a little bit more naive than we want for an initial solution =/
    # maybe try to do something along these lines but also implement dijkstra or something like that?
    # as in:  partition into three sets, and then for each set, go to the closest remaining unserved customer
    # until there are no customers remaining.
    # just a suggestion; y'all can be as creative as you want

    state = import_solution("C201_init_solution.txt")

    return state

init()

doAStar(initial_state())