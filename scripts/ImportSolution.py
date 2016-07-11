"""	Returns a State for a supplied solution
"""

from ImportCustomers import import_customers
from Depot import Depot
from Path import Path
from Truck import Truck
from State import State
from Visual import Visual
import argparse

path = '../standard_instances/'

def import_solution(filename):
    with open(path + filename) as f:
        customers = import_customers(filename.split("_")[0] + ".txt")
        lines = f.readlines()
        ids1 = lines[5].split()[3:]
        ids2 = lines[6].split()[3:]
        ids3 = lines[7].split()[3:]
        path1 = Path([])
        path2 = Path([])
        path3 = Path([])
    for id in ids1:
        path1.route.append(customers[int(id) - 1])
    for id in ids2:
        path2.route.append(customers[int(id) - 1])
    for id in ids3:
        path3.route.append(customers[int(id) - 1])

    print path1.calculate_distance() + path2.calculate_distance() + path3.calculate_distance()

    return State(Truck(1, 0, 0, 700, path=path1),
                 Truck(2, 0, 0, 700, path=path2),
                 Truck(3, 0, 0, 700, path=path3), parent=None)

parser = argparse.ArgumentParser()
parser.add_argument("filename")
args = parser.parse_args()
filename = args.filename

state = import_solution(filename)
#printing missed customers
Visual.plot_customers(Depot(0,0),state.truck1.path.is_valid())
Visual.plot_customers(Depot(0,0),state.truck2.path.is_valid())
Visual.plot_customers(Depot(0,0),state.truck3.path.is_valid())
Visual.show()
#printing number of missed customers
print len(state.truck1.path.is_valid()) + len(state.truck2.path.is_valid()) + len(state.truck3.path.is_valid())