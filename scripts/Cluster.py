import itertools
from Path import Path
from Customer import Customer

class Cluster():
    MAX_LEN_BRUTE_FORCE = 10

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

    # brute forces a solution if len(customers) <= n, can be overriden
    def get_solution(self, override = False):
        if len(self.customers) > self.MAX_LEN_BRUTE_FORCE and not override:
            return None

        min = -1
        best_path = Path(self.customers)
        for cs in itertools.permutations(self.customers):
            p = Path(cs)
            dist = p.distance
            if min == -1 or dist < min:
                min = dist
                best_path = p

        return best_path

    def get_cargo(self):
        sum_cargo = 0
        for customer in self.customers:
            sum_cargo += customer.demand
        return sum_cargo

    def get_radius(self):
        # farthest customer from the center, compares each customer x and y to the center...
        # replaces radius every time a bigger one is found
        center_x = self.get_center()[0]
        center_y = self.get_center()[1]
        new_farthest_distance = 0
        count = 0

        for c in self.customers:
            delta_x = c.x - center_x
            delta_y = c.y - center_y
            radius = ((delta_x**2)+(delta_y**2)) ** 0.5
            if radius > new_farthest_distance: 
                new_farthest_distance = radius
            else:
                new_farthest_distance = new_farthest_distance
            count += 1

        cluster_radius_final = new_farthest_distance

        return cluster_radius_final