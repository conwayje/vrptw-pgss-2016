from Customer import Customer
from Visual import Visual
from Depot import Depot
from ClusterSolutions import ClusterSolutions
path = '../standard_instances/'

customers = []

def import_customers(filename):
    with open(path + filename) as f:
        for i in xrange(6):
            f.next()
        for line in f:
            custList = line.replace('\n', '').split()
            # create temp customer to add to array; shift location so that it is relative to depot at 0,0
            temp = Customer(int(custList[0])-1, float(custList[1]) - 40, float(custList[2]) - 50, float(custList[4]), float(custList[5]), float(custList[6]), float(custList[3]))

            customers.append(temp)

    # assign clusters
    if filename == "C201.txt":
    	# if data needs to be accessed, for each cluster call custom_solution

    	c1 = ClusterSolution(1, [39,36,34,38,37,33,32,35,31], 0, 0, 0, 0)
    	## i.e. "c1.custom_solution"
    	c2 = ClusterSolution(2, [16,14,12,19,15,18,17,13], 0, 0, 0, 0)
    	c3 = ClusterSolution(3, [30,29,27,24,22,20,21], 0, 0, 0, 0)
    	c4 = ClusterSolution(4, [52,47,43,50,42,41,51,45], 0, 0, 0, 0)
    	c5 = ClusterSolution(5, [57,55,59,54,60,58,56,53], 0, 0, 0, 0)
    	c6 = ClusterSolution(6, [67,63,69,66,62,74,64,61,72], 0, 0, 0, 0)
    	c7 = ClusterSolution(7, [91,90,88,86,84,83,82], 0, 0, 0, 0)
    	c8 = ClusterSolution(8, [81,76,71,79,73,70,80], 0, 0, 0, 0)
    else if filename == "RC208.txt":
    	rc1 = ClusterSolution(1, [17,47,14,12,16,15,11,10,13,9], 0, 0, 0, 0)
    	rc2 = ClusterSolution(2, [5,3,1,45,8,46,4,7,6,2], 0, 0, 0, 0)
    	rc3 = ClusterSolution(3, [43,44,42,40,39,38,41,36,35,37], 0, 0, 0, 0)
    	rc4 = ClusterSolution(4, [34,31,29,27,32,30,28,26,33], 0, 0, 0, 0)
    	rc5 = ClusterSolution(5, [24,22,20,49,19,25,23,21,48,18], 0, 0, 0, 0)
    	    	

    return customers



# Visual.plot_customers(Depot(0,0), import_customers("C201.txt"))
# Visual.show()
