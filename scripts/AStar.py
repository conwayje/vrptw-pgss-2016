from heapq import *

def doAStar(initial_state):
    queue = []
    heappush(queue, (0, initial_state))
    world_record_not_broken = True

    while ( len(queue) > 0 ) and world_record_not_broken:
        (priority, state) = heappop(queue)

        if state.is_world_record():
            print "Yay"
            print state
            queue = []
            world_record_not_broken = False
            break

        for c in state.get_chidren():
            heappush(queue, ( c.score(), c) )

    return state


