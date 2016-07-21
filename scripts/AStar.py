from heapq import *
from HeuristicScore import score

def doAStar(initial_state, world_record = 591.55):
    queue = []

    heappush(queue, (score(initial_state), initial_state))
    world_record_not_broken = True

    initial_state.plot()
    print initial_state

    prev_scores = []
    diff = 0
    counter = 0
    average_rate = 0
    rate = 0

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


        print "Score of currently explored state: {}".format( priority )
        # if(priority < 10000000):
        print "Distance:", state.calculate_distance()

        if state.calculate_distance() < world_record:
            print "Yay"
            print state
            print state.get_score()

            # @TODO: truck number dependency
            # also, this is kind of messy generally...
            for truck in state.trucks:
                for c in truck.path.route:
                    print c.number,
            queue = []
            world_record_not_broken = False
            break

        # print state.get_score(), state
        children = state.get_children_small_moves()
        # print len(children)


        prev_scores.insert(0, priority)

        if (not len(prev_scores) <= 10):
            to_remove = prev_scores.pop()
            diff = priority - to_remove

        if len(prev_scores)>1:
            rate = priority - prev_scores[1]

        if counter != 0:
            average_rate = (rate + average_rate * (counter-1))/counter

        counter += 1
        print average_rate, diff

        if average_rate > -100000:
            queue = queue[100:]
            children = []
            children.append(state.get_children_big_moves())
            children.append((state.get_children_medium_moves()))



        for c in children:
            heappush(queue, ( score(c), c) )

        done = False
        while len(queue) > 0 and not done:
            (next, next_state) = queue[0]
            if next == priority:
                heappop(queue)
            else:
                done = True


    return state


