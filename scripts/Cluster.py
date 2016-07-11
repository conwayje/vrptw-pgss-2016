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
    def get_solution(self, override):
        if(len(self.customers) <= self.MAX_LEN_BRUTE_FORCE or override):
            return None

        min = -1
        best_path = Path(self.customers)
        for cs in itertools.permutations(self.customers):
            p = Path(cs)
            dist = p.calculate_distance()
            if(min == -1 or dist < min):
                min = dist
                best_path = p

        return best_path
        print (best_path)

    def get_data (self):
        sum_cargo = customers(self.demand)
        # farthest customer from the center, compares each customer x and y to the center...
        # replaces radius every time a bigger one is found
        center_x = total_x/count
        center_y = total_y/count
        new_farthest_distance = 0
        count = 0

        for c in self.customers:
            delta_x = c.x - center_x
            delta_y = c.y - center_y
            radius = ((delta_x**2)+(delta_y**2)) ** 0.5
            if radius > new_farthest_distance: 
                new_farthest_distance = radius;
            else:
                new_farthest_distance = new_farthest_distance
            count+= 1

        cluster_radius_final = new_farthest_distance

        return sum_cargo, cluster_radius_final
        print (sum_cargo)
        print (cluster_radius_final)
        print (center_x+ ", " + center_y)
        
    # old method to get perms, but python already has one
    # @staticmethod
    # def generate_perms(customers):
    #     perms = []
    #     if len(customers) == 1:
    #         return customers
    # @TODO -- this might also need the problem definition name [rc208, c201, or whatever]
    # in order to properly decide which customers are clustered.  also ask @suvir if you
    # need help visualizing.
    #
    # personal request:  keep clusters small so that [cluster].get_solution() is useful more often
    # than not =)
    @staticmethod
    def create_clusters(customers):
        pass
