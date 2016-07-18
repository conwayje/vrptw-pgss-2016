# Heuristic Scoring
## Penalize for bad moves, reward for good moves (or for not being penalized)
from Path import Path
from Customer import Customer
from Truck import Truck

## STILL NEED PENALTIES FOR COMING OUT OF CLUSTERS AND OUTRAGEOUS ANGLE OF TURNING

class Heuristic_Score():
    def _init_(self, state):
        self.state = state


    def penalties(self):
        score = 0

        # placeholder paths until state is generated
        paths = self.state.get_paths
        # get the distance (benchmark score) from paths
        distance = paths.distance

        score += distance
        for path in paths:
            # ya done goofed
            score += 1000000000 * len(path.is_valid())

        return score
        # #if (did_cross == True):
        # #	distance += 100

        # if (capacity == 0):
        # 	# if the capacity of the truck reaches 0 at any time
        # 	distance += 500

        # if (diff_time > 0):
        # 	distance += early_arrival/2

        # for(customer in self.truck.path.route)
        # {

        # }
