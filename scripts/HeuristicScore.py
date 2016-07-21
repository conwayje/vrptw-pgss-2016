# Heuristic Scoring
## Penalize for bad moves, reward for good moves (or for not being penalized)
from Path import Path
from Customer import Customer
from Truck import Truck

## STILL NEED PENALTIES FOR COMING OUT OF CLUSTERS AND OUTRAGEOUS ANGLE OF TURNING

        
def score(state):
    score = 0

    # placeholder paths until state is generated
    paths = state.paths
    # get the distance (benchmark score) from paths
    distance = state.calculate_distance()

    score += distance
    for path in paths:
        # ya done goofed
        # The following is for not hitting a customer 

        score += 1000000 * len(path.is_valid())
        #If the path ever crosses itself 
        score += 10 * path.intersects_self()
        #The following is for hitting a customer, but not having enough cargo 
        score += 5000 * ( len(path.route ) - path.get_indice_customer_missed(state.truck1.cargo))
        # The following is a penalty for each minute spent waiting 

        score += 5000 * ( len(path.route ) - path.get_indice_customer_missed(state.trucks[0].cargo))
        score += 5 * path.get_wait_time()

    return score

    

