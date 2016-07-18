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
            score += 1000000 * len(path.is_valid())
            score += 10 * path.intersects_self()
            score += 1000 * ( len(path.route() ) - len( path.get_indice_customer_missed()) )
            score += 5 * path.get_waittime()

        return score
        
	def score(state):
	    score = 0

	    # placeholder paths until state is generated
	    paths = state.paths
	    # get the distance (benchmark score) from paths
	    distance = state.calculate_distance()

	    score += distance
	    for path in paths:
	        # ya done goofed
	        score += 1000000 * len(path.is_valid())
	        score += 1000 * path.intersects_self()
	        score += 5000 * ( len(path.route ) - path.get_indice_customer_missed(state.truck1.cargo))
	        score += 50 * path.get_wait_time()

	    return score

    

       

        
        # for(customer in self.truck.path.route)
        # {

        # }
