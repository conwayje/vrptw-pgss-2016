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
    global penalty_weights
    if mode == 0:
        # base scoring mode
        penalty_weights["Distance"] = 3000
        penalty_weights["Missed Time"] = 1000000
        penalty_weights["Missed Cargo"] = 5
        penalty_weights["Wait Time"] = 10
        penalty_weights["Excessive Waits"] = 100
        penalty_weights["Unreasonable Distances"] = 500
        penalty_weights["Intraintersections"] = 50
        penalty_weights["Interintersections"] = 200
    elif mode == 1:
        # focus a lot on intersections
        penalty_weights["Distance"] = 3000
        penalty_weights["Missed Cargo"] = 5
        penalty_weights["Wait Time"] = 10
        penalty_weights["Excessive Waits"] = 100
        penalty_weights["Unreasonable Distances"] = 500
        penalty_weights["Missed Time"] = 10000
        penalty_weights["Intraintersections"] = 500
        penalty_weights["Interintersections"] = 2000
    elif mode == 2:
        # focus a lot on distance and nothing else
        penalty_weights["Distance"] = 3000
        penalty_weights["Missed Cargo"] = 5
        penalty_weights["Wait Time"] = 10
        penalty_weights["Excessive Waits"] = 10
        penalty_weights["Unreasonable Distances"] = 50
        penalty_weights["Missed Time"] = 1000
        penalty_weights["Interintersections"] = 50
        penalty_weights["Intraintersections"] = 20
    elif mode == 3:
        # focus a lot on unreasonable distance and nothing else
        penalty_weights["Distance"] = 100
        penalty_weights["Missed Cargo"] = 5
        penalty_weights["Wait Time"] = 10
        penalty_weights["Excessive Waits"] = 10
        penalty_weights["Unreasonable Distances"] = 100000
        penalty_weights["Missed Time"] = 100
        penalty_weights["Interintersections"] = 50
        penalty_weights["Intraintersections"] = 20

## STILL NEED PENALTIES FOR COMING OUT OF CLUSTERS AND OUTRAGEOUS ANGLE OF TURNING
def score(state):
    paths = state.paths
    n_customers = len( Distances.matrix[0] ) - 1
    cargo = state.trucks[0].cargo

    num_intersections = 0

    # Add the distance (benchmark score) from paths
    score = state.calculate_distance() * penalty_weights["Distance"]

    for path in paths:
        stats = path.combined_stats(cargo)

        # Missed customers by time
        ## The missed_cust_penalty variable is to avoid a number dependency in the AStar.py method handle_world_record
        score += penalty_weights["Missed Time"] * stats["Missed Time"] #DONE

        # Intersecting self
        path.intersects_self()
        num_intersections += path.number_intersections()

        # Missed customers by cargo
        score += penalty_weights["Missed Cargo"] * stats["Missed Cargo"] #DONE

        # Total wait time
        score += penalty_weights["Wait Time"] * stats["Wait Time"] #DONE

        # Excessive waiting
        score += penalty_weights["Excessive Waits"] * stats["Excessive Waits"] #DONE

        # extra penalty for large distance between two computers
        score += penalty_weights["Unreasonable Distances"] * stats["Unreasonable Distances"] #DONE

    # for every 8 customers, you get 1 intersection for free.  after that, it costs you.
    if (num_intersections > ( n_customers / 10 ) ):
        score += penalty_weights["Intraintersections"] * ( num_intersections - ( n_customers / 10 ) )

    # for i in range(len(paths)):
    #     for j in range(i+1, len(paths)):
    #         score += penalty_weights["Interintersections"] * len(paths[i].intersects_with_other(paths[j]))

    return score

def print_score_vals(state):
    missed_time = 0
    missed_cargo = 0
    wait_time = 0
    excessive_waits = 0
    num_intersections = 0
    num_unreasonable_distances = 0
    num_customers = 0
    cargo = state.trucks[0].cargo

    for path in state.paths:
        stats = path.combined_stats(cargo)
        # Number Customers
        num_customers += len(path.route)
        # Missed customers by time
        missed_time += stats["Missed Time"]
        # Intersecting self
        num_intersections += path.number_intersections()
        # Missed customers by cargo
        missed_cargo += stats["Missed Cargo"]
        # Total wait time
        wait_time += stats["Wait Time"]
        # Penalize excessive waiting
        excessive_waits += stats["Excessive Waits"]
        # extra penalty for large distance between two computers
        num_unreasonable_distances += stats["Unreasonable Distances"]

    for i in range(len(state.paths)):
        for j in range(i+1, len(state.paths)):
            num_intersections += len(state.paths[i].intersects_with_other(state.paths[j]))

    print "Number Customers:         {0:>4}".format(num_customers)
    print "Missed customers (time):  {0:>4} \nMissed customers (cargo): {1:>4} \nNumIntersections:         {2:>4} \n" \
          "Wait time:                {3:>4} \nNumUnreasonable:          {0:>4} \nExcessive Waits:          {2:>4}"\
          .format(missed_time, missed_cargo, num_intersections, int(wait_time), num_unreasonable_distances)