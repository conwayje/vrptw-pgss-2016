import numpy as np
from Customer import Customer

path = 'standard_instances/'

customers = []
    
def import_customers(filename):
    f = open(path + "C201.txt", 'r')
    with open(path + "C201.txt") as f:
        for i in xrange(6):
            f.next()
        for line in f:
            custList = line.replace('\n', '').split()
            #create temp customer to add to array; shift location so that it is relative to depot at 0,0
            temp = Customer(int(custList[0])-1, int(float(custList[1])) - 40, int(float(custList[2])) - 50, custList[4], custList[5], custList[6], custList[3])
            #print temp
            customers.append(temp)
            
    #print customers  
    return customers   

import_customers("C201.txt")