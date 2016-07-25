# Heuristic Scoring
## Penalize for bad moves, reward for good moves (or for not being penalized)
from Path import Path
from Customer import Customer
from Truck import Truck

## STILL NEED PENALTIES FOR COMING OUT OF CLUSTERS AND OUTRAGEOUS ANGLE OF TURNING
def score(state):
    score = 0
    paths = state.paths
    cargo = state.trucks[0].cargo

    # Add the distance (benchmark score) from paths
    score += state.calculate_distance()

    for path in paths:
        # Missed customers by time
        score += 1000000 * path.number_missed_by_time()
        # Intersecting self
        score += 10 * path.intersects_self()
        # Missed customers by cargo
        score += 5000 * path.number_missed_by_cargo(cargo)
        # Total wait time
        score += 5 * path.get_wait_time()

    return score