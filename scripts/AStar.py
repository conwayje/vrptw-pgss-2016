from heapq import *
from HeuristicScore import score

def doAStar(initial_state, world_record = 591.55):
    queue = []

    heappush(queue, (0, initial_state))
    world_record_not_broken = True

    while ( len(queue) > 0 ) and world_record_not_broken:
        print len(queue)
        while(len(queue) > 10000):
            extra = queue.pop()
            del extra

        (priority, state) = heappop(queue)

        print "Score of currently explored state: {}".format( priority )
        # if(priority < 10000000):
        #     state.plot()

        if state.calculate_distance()< world_record:
            print "Yay"
            print state
            print state.get_score()

            # @TODO: truck number dependency
            # also, this is kind of messy generally...
            for c in state.truck1.path.route:
                print c.number,
            print
            for c in state.truck2.path.route:
                print c.number,
            print
            for c in state.truck3.path.route:
                print c.number,
            queue = []
            world_record_not_broken = False
            break

        # print state.get_score(), state
        children = state.get_children()
        # print len(children)

        for c in children:
            heappush(queue, ( score(c), c) )

    return state


