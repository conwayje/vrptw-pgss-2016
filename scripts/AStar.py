from heapq import *

def doAStar(initial_state):
    queue = []
    heappush(queue, (0, initial_state))
    world_record_not_broken = True

    while ( len(queue) > 0 ) and world_record_not_broken:
        (priority, state) = heappop(queue)

        print "Score of currently explored state: {}".format( priority )

        if state.is_world_record():
            print "Yay"
            print state
            queue = []
            world_record_not_broken = False
            break

        # print state.get_score(), state
        children =state.get_children()
        # print len(children)
        for c in children:
            heappush(queue, ( c.get_score(), c) )
    
    return state


