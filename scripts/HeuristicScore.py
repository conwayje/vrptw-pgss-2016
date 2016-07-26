# Heuristic Scoring
## Penalize for bad moves, reward for good moves (or for not being penalized)
from Path import Path
from Customer import Customer
from Truck import Truck
from Distances import Distances
try:
    import ipdb
except:
    print "Skipping ipdb import because Dan's school is full of jerks"

## STILL NEED PENALTIES FOR COMING OUT OF CLUSTERS AND OUTRAGEOUS ANGLE OF TURNING
def score(state):
    score = 0
    missed_cust_penalty = 1000000
    paths = state.paths
    n_customers = len( Distances.matrix[0] ) - 1
    cargo = state.trucks[0].cargo

    # Add the distance (benchmark score) from paths
    score += state.calculate_distance() * 3000
    num_intersections = 0;
    for path in paths:
        # run the intersecting paths algorithm once, which saves it on the instance,
        # preventing you from having to run it several times
        path.intersects_self()

        # Missed customers by time
        ## The missed_cust_penalty variable is to avoid a number dependency in the AStar.py method handle_world_record
        score += missed_cust_penalty * path.number_missed_by_time()
        # Intersecting self
        num_intersections += len( path.intersecting_segments )
        # Missed customers by cargo
        score += 5 * path.number_missed_by_cargo(cargo)
        # Total wait time
<<<<<<< HEAD
        score += 5 * path.get_wait_time()
=======
        score += 10 * path.get_wait_time()
        # ipdb.set_trace()
>>>>>>> 816961b3e69e8502f2ca3a1682de4d78b1d2e1ff
        # Excessive waiting
        score += 100 * path.get_number_of_excessive_waits()
        # extra penalty for large distance between two computers
        score += 500 * path.num_unreasonable_distances()

    # for every 8 customers, you get 1 intersection for free.  after that, it costs you.
    if (num_intersections > ( n_customers / 10 ) ):
        score += 200 * ( num_intersections - ( n_customers / 10 ) )

    for i in range(len(paths)):
        for j in range(i+1, len(paths)):
            score += 50 * len(paths[i].intersects_with_other(paths[j]))

    return score
#
# Possible Heuristic score to use
# for path in paths:
#     # run the intersecting paths algorithm once, which saves it on the instance,
#     # preventing you from having to run it several times
#     path.intersects_self()
#
#     # Missed customers by time
#     score += 1000 * path.number_missed_by_time()
#     # Intersecting self
#     num_intersections += 100 * len( path.intersecting_segments )
#     # Missed customers by cargo
#     score += 1000 * path.number_missed_by_cargo(cargo)
#     # Total wait time
#     score += path.get_wait_time()
#     # extra penalty for large distance between two computers
#     score += 50 * path.num_unreasonable_distances()
#
# for i in range(len(paths)):
#     for j in range(i + 1, len(paths)):
#         score += 50 * len(paths[i].intersects_with_other(paths[j]))
#
# if (num_intersections > 10):
#     score += num_intersections * 50


def print_score_vals(state):
    missed_time = 0
    missed_cargo = 0
    wait_time = 0
    num_intersections = 0
    num_unreasonable_distances = 0
    for path in state.paths:
        # Missed customers by time
        missed_time += path.number_missed_by_time()
        # Intersecting self
        num_intersections += path.number_intersections()
        # Missed customers by cargo
        missed_cargo +=  path.number_missed_by_cargo(state.trucks[0].cargo)
        # Total wait time
        wait_time += path.get_wait_time()
        # Penalize excessive waiting
        excessive_wait += path.get_number_of_excessive_waits()
        # extra penalty for large distance between two computers
        num_unreasonable_distances +=  path.num_unreasonable_distances()

    for i in range(len(state.paths)):
        for j in range(i+1, len(state.paths)):
            num_intersections += len(state.paths[i].intersects_with_other(state.paths[j]))

    print "Missed customers (time):  {0:>4} \nMissed customers (cargo): {1:>4} \nNumIntersections:         {2:>4} \n" \
          "Wait time:                {3:>4} \nNumUnreasonable:          {0:>4}"\
          .format(missed_time, missed_cargo, num_intersections, int(wait_time), num_unreasonable_distances)


