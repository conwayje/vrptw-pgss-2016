# SolutionReader.py

from ImportCustomers import import_customers
from Depot import Depot
from Path import Path
from Truck import Truck
from State import State

path = '../standard_instances/'
customers = []


def import_solution(solutionFile, customers):
    with open(path + solutionFile) as f:
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

    print path1.get_distance() + path2.get_distance() + path3.get_distance()

    return State(Truck(1, 0, 0, path=path1),
                 Truck(2, 0, 0, path=path2),
                 Truck(3, 0, 0, path=path3), parent=None)
