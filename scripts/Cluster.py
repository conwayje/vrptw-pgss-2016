import itertools
from Path import Path

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
            dist = p.get_distance()
            if(min == -1 or dist < min):
                min = dist
                best_path = p

        return best_path


    # @TODO -- this might also need the problem definition name [rc208, c201, or whatever]
    # in order to properly decide which customers are clustered.  also ask @suvir if you
    # need help visualizing.
    #
    # personal request:  keep clusters small so that [cluster].get_solution() is useful more often
    # than not =)
    @staticmethod
    def create_clusters(customers):
        pass
