from Customer import Customer
from Visual import Visual
from Depot import Depot

path = '../standard_instances/'

customers = []

def import_customers(filename):
    with open(path + filename) as f:
        for i in xrange(6):
            f.next()
        for line in f:
            custList = line.replace('\n', '').split()
            #create temp customer to add to array; shift location so that it is relative to depot at 0,0
            temp = Customer(int(custList[0])-1, float(custList[1]) - 40, float(custList[2]) - 50, float(custList[4]), float(custList[5]), float(custList[6]), float(custList[3]))

            customers.append(temp)

    return customers

# Visual.plot_customers(Depot(0,0), import_customers("C201.txt"))
# Visual.show()