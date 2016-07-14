from Customer import Customer
from Visual import Visual
from Depot import Depot
from ClusterSolution import ClusterSolution

path = '../standard_instances/'

customers = []

def import_customers(filename):
    with open(path + filename) as f:
        for i in xrange(6):
            f.next()
        for line in f:
            custList = line.replace('\n', '').split()
            # create temp customer to add to array; shift location so that it is relative to depot at 0,0
            temp = Customer(int(custList[0]) - 1, float(custList[1]) - 40, float(custList[2]) - 50, float(custList[4]),
                            float(custList[5]), float(custList[6]), float(custList[3]))

            customers.append(temp)

    # assign clusters
    if filename == "C201.txt":
        # if data needs to be accessed, for each cluster call custom_solution, i.e. "c1.custom_solution"
        c1 = ClusterSolution(1, [customers[i - 1] for i in [39, 36, 34, 38, 37, 33, 32, 35, 31]])
        c2 = ClusterSolution(2, [customers[i - 1] for i in [16, 14, 12, 19, 15, 18, 17, 13]])
        c3 = ClusterSolution(3, [customers[i - 1] for i in [30, 29, 27, 24, 22, 20, 21]])
        c4 = ClusterSolution(4, [customers[i - 1] for i in [52, 47, 43, 50, 42, 41, 51, 45]])
        c5 = ClusterSolution(5, [customers[i - 1] for i in [57, 55, 59, 54, 60, 58, 56, 53]])
        c6 = ClusterSolution(6, [customers[i - 1] for i in [67, 63, 69, 66, 62, 74, 64, 61, 72]])
        c7 = ClusterSolution(7, [customers[i - 1] for i in [91, 90, 88, 86, 84, 83, 82]])
        c8 = ClusterSolution(8, [customers[i - 1] for i in [81, 76, 71, 79, 73, 70, 80]])
    elif filename == "RC208.txt":
        rc1 = ClusterSolution(1, [17, 47, 14, 12, 16, 15, 11, 10, 13, 9])
        rc2 = ClusterSolution(2, [customers[i - 1] for i in [5, 3, 1, 45, 8, 46, 4, 7, 6, 2]])
        rc3 = ClusterSolution(3, [customers[i - 1] for i in [43, 44, 42, 40, 39, 38, 41, 36, 35, 37]])
        rc4 = ClusterSolution(4, [customers[i - 1] for i in [34, 31, 29, 27, 32, 30, 28, 26, 33]])
        rc5 = ClusterSolution(5, [customers[i - 1] for i in [24, 22, 20, 49, 19, 25, 23, 21, 48, 18]])

    return customers

# Visual.plot_customers(Depot(0,0), import_customers("C201.txt"))
# Visual.show()