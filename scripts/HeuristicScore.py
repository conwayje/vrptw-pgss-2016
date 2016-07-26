# Heuristic Scoring
## Penalize for bad moves, reward for good moves (or for not being penalized)
from Path import Path
from Customer import Customer
from Truck import Truck
from Distances import Distances
from time import time
try:
    import ipdb
except:
    print "Skipping ipdb import because Dan's school is full of jerks"

penalty_weights = {}

DEFAULT = 0
FIX_INTERSECTIONS = 1
FIX_UNREASONABLE_DISTANCES = 2

def set_score_mode(mode = DEFAULT):
    if mode == 1:
        set_score_mode(DEFAULT)
        penalty_weights["Missed Time"] = 10000
        penalty_weights["Interintersections"] = 500
        penalty_weights["Intraintersections"] = 2000
    if mode == 2:
        set_score_mode(DEFAULT)
        penalty_weights["Missed Time"] = 10000
        penalty_weights["Unreasonable Distances"] = 5000
    else:
        penalty_weights["Distance"] = 3000
        penalty_weights["Missed Time"] = 1000000
        penalty_weights["Missed Cargo"] = 5
        penalty_weights["Wait Time"] = 10
        penalty_weights["Excessive Weights"] = 100
        penalty_weights["Unreasonable Distances"] = 500
        penalty_weights["Intraintersections"] = 200
        penalty_weights["Interintersections"] = 50




## STILL NEED PENALTIES FOR COMING OUT OF CLUSTERS AND OUTRAGEOUS ANGLE OF TURNING
def score(state):

    paths = state.paths
    n_customers = len( Distances.matrix[0] ) - 1
    cargo = state.trucks[0].cargo

    num_intersections = 0

    # Add the distance (benchmark score) from paths
    score = state.calculate_distance() * penalty_weights["Distance"]


    for path in paths:
        # Missed customers by time
        ## The missed_cust_penalty variable is to avoid a number dependency in the AStar.py method handle_world_record
        score += penalty_weights["Missed Time"] * path.number_missed_by_time()

        # Intersecting self
        path.intersects_self()
        num_intersections += len( path.intersecting_segments )

        # Missed customers by cargo
        score += penalty_weights["Missed Cargo"] * path.number_missed_by_cargo(cargo)

        # Total wait time
        score += penalty_weights["Wait Time"] * path.get_wait_time()

        # Excessive waiting
        score += penalty_weights["Excessive Weights"] * path.get_number_of_excessive_waits()

        # extra penalty for large distance between two computers
        score += penalty_weights["Unreasonable Distances"] * path.num_unreasonable_distances()

    # for every 8 customers, you get 1 intersection for free.  after that, it costs you.
    if (num_intersections > ( n_customers / 10 ) ):
        score += penalty_weights["Intraintersections"] * ( num_intersections - ( n_customers / 10 ) )

    for i in range(len(paths)):
       for j in range(i+1, len(paths)):
           score += penalty_weights["Interintersections"] * len(paths[i].intersects_with_other(paths[j]))

    return score

def print_score_vals(state):
    missed_time = 0
    missed_cargo = 0
    wait_time = 0
    excessive_waits = 0
    num_intersections = 0
    num_unreasonable_distances = 0
    num_customers = 0


    for path in state.paths:
        # Number Customers
        num_customers += len(path.route)
        # Missed customers by time
        missed_time += path.number_missed_by_time()
        # Intersecting self
        num_intersections += path.number_intersections()
        # Missed customers by cargo
        missed_cargo +=  path.number_missed_by_cargo(state.trucks[0].cargo)
        # Total wait time
        wait_time += path.get_wait_time()
        # Penalize excessive waiting
        excessive_waits += path.get_number_of_excessive_waits()
        # extra penalty for large distance between two computers
        num_unreasonable_distances +=  path.num_unreasonable_distances()

    for i in range(len(state.paths)):
        for j in range(i+1, len(state.paths)):
            num_intersections += len(state.paths[i].intersects_with_other(state.paths[j]))

    print "Number Customers:         {0:>4}".format(num_customers)
    print "Missed customers (time):  {0:>4} \nMissed customers (cargo): {1:>4} \nNumIntersections:         {2:>4} \n" \
          "Wait time:                {3:>4} \nNumUnreasonable:          {0:>4} \nExcessive Waits:          {2:>4}"\
          .format(missed_time, missed_cargo, num_intersections, int(wait_time), num_unreasonable_distances)


