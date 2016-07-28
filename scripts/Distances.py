from Customer import Customer
from ImportCustomers import import_customers

class Distances():
    
    matrix = []

    @staticmethod
    def calculate_matrix(customers):
        customers = sorted(customers, key = lambda customer: customer.number)
        customers.insert(0, Customer(0, 0, 0, 0, 0, 0, 0))
        for c1 in customers:
            row = []
            for c2 in customers:
                row.append(c1.distance_to_customer(c2))
            Distances.matrix.append(row)
#        return Distances.matrix

    @staticmethod
    def get_distance(c1, c2):
        return Distances.matrix[c1][c2]

    @staticmethod
    def get_closest_customers(customer):
        return sorted(range(1, 101), key = lambda cust: Distances.matrix[customer.number][cust])

#testing
# customers = import_customers("RC208.txt", False)
# print "Calculating distances..."
# Distances.calculate_matrix(customers)
# print Distances.get_closest_customers(customers[5])
