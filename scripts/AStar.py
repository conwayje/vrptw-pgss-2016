from heapq import *
from HeuristicScore import score

def doAStar(initial_state, world_record = 591.55 ):
    queue = []

    heappush(queue, (score(initial_state), initial_state))
    world_record_not_broken = True

    print initial_state

    prev_scores = []
    diff = -100000000
    counter = 0
    average_rate = -1000000
    rate = 0

    try:
        while ( len(queue) > 0 ) and world_record_not_broken:
            while(len(queue) > 10000):
                extra = queue.pop()
                del extra

            (priority, state) = heappop(queue)

            done = False
            while len(queue) > 0 and not done:
                (next, next_state) =  queue[0]
                if next == priority:
                    heappop(queue)
                else:
                    done = True

            print "Score: {0:<20,} Distance: {1:<20}".format( priority, state.calculate_distance(), grouping = True )

            if state.calculate_distance() < world_record:
                print "Yay"
                print state
                print state.get_score()
                for truck in state.trucks:
                    for c in truck.path.route:
                        print c.number,

                    print
                queue = []
                world_record_not_broken = False
                break


            prev_scores.insert(0, priority)

            if (not len(prev_scores) <= 10):
                to_remove = prev_scores.pop()
                diff = priority - to_remove

            children = []
            if len(prev_scores)>1:
                if(priority - prev_scores[0] < 10000000):
                    children = state.get_children(True, True, True)
                else:
                    children = state.get_children(True, True, False)

            if counter != 0:
                average_rate = (rate + average_rate * (counter-1))/counter

            counter += 1

            for c in children:
                heappush(queue, ( score(c), c) )

            done = False
            while len(queue) > 0 and not done:
                (next, next_state) = queue[0]
                if next == priority:
                    heappop(queue)
                else:
                    done = True
    except KeyboardInterrupt:
        print "Stopping"
    return state

