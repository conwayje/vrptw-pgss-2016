class Distances():

    def __init__(self, customers):
        self.matrix = []

        customers = sorted(customers, key = lambda customer: customer.number)
        for c1 in customers:
            row = []
            for c2 in customers:
                row.append(c1.distance_to_customer(c2))
            self.matrix.append(row)


