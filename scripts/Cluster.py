class Cluster():

    def __init__(self, customers):
        self.customers = customers

    # Returns the center, simply the mean of all the customer coordinates
    def get_center(self):
        total_x = 0
        total_y = 0
        count = 0
        for c in self.customers:
            total_x += c.x
            total_y += c.y
            count += 1
        return (total_x/count, total_y/count)

    def getSolution(self):
        pass # will return a path, probably brute forced here, as long as len(customers) < a

    @staticmethod
    def create_clusters(customers):
        pass
