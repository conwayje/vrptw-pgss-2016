from Customer import Customer

class Distances():

    matrix = []

    # @TODO -- I think this should also include the depot at 0 such that if c1.number = x and c2.number = y
    # then we can get their distance at [x][y] instead of at [x-1][y-1]
    @staticmethod
    def calculate_matrix(customers):
        customers = sorted(customers, key = lambda customer: customer.number)
        # @TODO -- wait, why are we creating more customers?  ((o_O))
        customers.insert(0, Customer(0, 0, 0, 0, 0, 0, 0))
        for c1 in customers:
            row = []
            for c2 in customers:
                row.append(c1.distance_to_customer(c2))
            Distances.matrix.append(row)
#        return Distances.matrix

    # @TODO -- does this return what you think it would?  if you pass in cust #1 and cust #2, don't you get
    # the distance from cust 2 to cust 3?
    @staticmethod
    def get_distance(c1, c2):
        return Distances.matrix[c1][c2]
