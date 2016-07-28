from heapq import *
from HeuristicScore import *
from collections import deque
from random import random
from KeyPoller import KeyPoller
from ImportSolution import write_solution
from time import time
import datetime

try:
    import ipdb
except:
    print "Skipping import of ipdb because Dan's school is full of jerks"

def doAStar(initial_state, do_plot, world_record):
    queue = []

    #options for output
    display_customer_nums = False
    display_vals = False

    set_score_mode(DEFAULT)

    generation = 0

    # if you see something with an identical score as before, 99% chance it's the same state.  keep a set
    # of these guys and don't go in loops considering them again
    SEEN_SCORES = set()

    STATE_QUEUE_MAX_LENGTH = 1000

    QUEUE_LENGTH_EARLY_GAME = 150  # also acts as the # of generations before a reset is triggered
    RESET_TRIGGER_DIFFERENTIAL_SCORE_EARLY_GAME = 1000000

    QUEUE_LENGTH_LATE_GAME = 500  # same; also acts as # of gen. before a reset
    RESET_TRIGGER_DIFFERENTIAL_SCORE_LATE_GAME = 3

    IS_EARLY_GAME = True  # set this to false whenever the score drops below threshold
    EARLY_GAME_SCORE_THRESHOLD = 1000000

    heappush(queue, (score(initial_state), initial_state))
    world_record_not_broken = True

    previous_scores = deque([], QUEUE_LENGTH_EARLY_GAME)

    terminated = False
    with KeyPoller() as keyPoller:
        while (len(queue) > 0) and world_record_not_broken and not terminated:
            try:
                # clear anything that's ranked very poorly (saves memory; improves performance a bit)
                while (len(queue) > STATE_QUEUE_MAX_LENGTH):
                    e = queue.pop()
                    del e

                # get the score and state from the heap
                (priority, state) = heappop(queue)
                while priority in SEEN_SCORES:
                    del state
                    (priority, state) = heappop(queue)

                if priority < EARLY_GAME_SCORE_THRESHOLD and IS_EARLY_GAME:
                    # if we go from early game to late game, update some shit
                    IS_EARLY_GAME = False
                    QUEUE_LENGTH_EARLY_GAME += 20
                    previous_scores = deque([], QUEUE_LENGTH_LATE_GAME)
                    SEEN_SCORES = set()
                elif priority > EARLY_GAME_SCORE_THRESHOLD and not IS_EARLY_GAME:
                    # if we go from late game to early game, update some shit
                    IS_EARLY_GAME = True
                    QUEUE_LENGTH_EARLY_GAME += 20
                    previous_scores = deque([], QUEUE_LENGTH_EARLY_GAME)
                    SEEN_SCORES = set()

                # shove the score into the FIFO queue
                previous_scores.append(priority)

                # also update the set of seen scores
                SEEN_SCORES.add( priority )

                print "Gen {0:>6}: Score: {1:<25,} Distance: {2:<25}".format(generation, priority,
                                                                             state.calculate_distance(), grouping=True)

                if state.calculate_distance() < world_record:
                    if len( [ 1 for path in state.paths if path.missed_customers() == [] ] ) == len( state.paths ):
                        ## the score value is dependent on the value in heuristic score, change to 'missed_cust_penalty'
                        ## if the score is less than the penalty for missing a customer, then the solution is valid
                        ## the world record is broken and the solution is valid
                        handle_world_record(state)
                        world_record_not_broken = False
                        queue = []
                        break

                # logic for getting children...
                # usually, get medium and small.  SOMETIMES get the big ones, too, but not too many of them
                # if we're doing poorly, just get the big moves and get a lot of them
                if IS_EARLY_GAME:
                    if previous_scores[0] - previous_scores[-1] > RESET_TRIGGER_DIFFERENTIAL_SCORE_EARLY_GAME or len(
                            previous_scores) < QUEUE_LENGTH_EARLY_GAME:
                        # keep operating as usual
                        children = state.get_children(False, True, True, False, priority < 5000000)
                    else:
                        # uh oh, fucked up and didn't make progress in 300 moves in the early game.
                        # time to clear the queues and start over from the current state.
                        print "Forcing early-game reset..."
                        queue = []
                        QUEUE_LENGTH_EARLY_GAME += 20
                        previous_scores = deque([], QUEUE_LENGTH_EARLY_GAME)
                        SEEN_SCORES = set()
                        children = state.get_children(True, False, False, True)

                else:
                    if previous_scores[0] - previous_scores[-1] > RESET_TRIGGER_DIFFERENTIAL_SCORE_LATE_GAME or len(
                            previous_scores) < QUEUE_LENGTH_LATE_GAME:
                        children = state.get_children(False, True, True, False, priority < 5000000)
                    else:
                        # uh oh, fucked up and didn't make progress in 1000 moves in the late game.
                        # time to clear the queues and start over from the current state.
                        print "Forcing late-game reset..."
                        queue = []
                        QUEUE_LENGTH_EARLY_GAME += 20
                        previous_scores = deque([], QUEUE_LENGTH_EARLY_GAME)
                        SEEN_SCORES = set()
                        children = state.get_children(True, False, False, True)


                poll = keyPoller.poll()
                if not poll is None:
                    if poll == "s":
                        filename = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
                        print "Saving state to " + filename + ".txt"
                        write_solution(state, filename)
                    if poll == "v":
                        display_vals = True
                    if poll == "c":
                        display_vals = False
                    if poll == "z":
                        display_customer_nums = True
                    if poll == "x":
                        display_customer_nums = False
                    if poll == "p":
                        raw_input("Hit Enter to continue")
                    if poll == "q":
                        print "Quitting due to q button press"
                        import sys
                        sys.exit(0)

                    if poll.isdigit():
                        set_score_mode(int(poll))
                        queue = []
                        QUEUE_LENGTH_EARLY_GAME += 20
                        previous_scores = deque([], QUEUE_LENGTH_EARLY_GAME)
                        SEEN_SCORES = set()

                    if poll == "n":
                        print "Nuking children"
                        if (len(queue) > 100):
                            queue = queue[-100:]

                for c in children:
                    heappush(queue, (score(c), c))

                # is this useful?
                done = False
                while len(queue) > 0 and not done:
                    (next, next_state) = queue[0]
                    if next == priority:
                        heappop(queue)
                    else:
                        done = True

                if do_plot:
                    state.plot()

                generation += 1

            except KeyboardInterrupt:
                # if you use Ctrl+C, print out all the truck info
                # and then legitimately kill the program
                for truck in state.trucks:
                    for Customer in truck.path.route:
                        print Customer.number,
                    print

                break

            if (display_vals):
                print_score_vals(state)

            if (display_customer_nums):
                for truck in state.trucks:
                    for Customer in truck.path.route:
                        print Customer.number,
                    print

    return state


def handle_world_record(state):
    try:
        for x in range(5):
            print "###############################################"
        print "### World record solution was found"
        for x in range(5):
            print "###############################################"

        print state
        print state.get_score()

        for truck in state.trucks:
            print "T: ",
            for c in truck.path.route:
                print c.number,
            print

    except KeyboardInterrupt as e:
        print "Stopping"

    return state