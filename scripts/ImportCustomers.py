from Customer import Customer
#from ClusterSolution import ClusterSolution


customers = []

def import_customers(filename, is_test):
    
    if is_test:
        path = '../test_instances/'
    else:
        path = '../standard_instances/'
    with open(path + filename) as f:
        for i in xrange(5):
            f.next()
        depot_data = f.next().replace('\n', '').split()
        depot_x = float(depot_data[1])
        depot_y = float(depot_data[2])
        for line in f:
            custList = line.replace('\n', '').split()
            # create temp customer to add to array; shift location so that it is relative to depot at 0,0
            temp = Customer(int(custList[0]) - 1, float(custList[1]) - depot_x, float(custList[2]) - depot_y, float(custList[4]),
                            float(custList[5]), float(custList[6]), float(custList[3]))
            customers.append(temp)

    return customers

