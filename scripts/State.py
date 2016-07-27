from Visual import Visual
from Truck import Truck
import copy
from HeuristicScore import score
from Dijkstra import Dijsktra
from Path import Path
from Depot import Depot
##from ImportCustomers import ImportCustomers
from ClusterStore import ClusterStore
from random import randint, randrange, choice
from Distances import Distances
from Customer import Customer
import random
try:
    import ipdb
except:
    print "Skipping ipdb import because Dan's school is full of jerks"
import argparse

path = '../standard_instances/'

from time import time

class State():

    def __init__(self, trucks, parent = None):

        self.trucks = trucks
        self.paths = [truck.path for truck in trucks]

        self.distance = None
        self.parent = parent

    def calculate_distance(self):
        self.distance = 0
        for truck in self.trucks:
            self.distance += truck.path.calculate_distance()
        return self.distance

    def plot(self):
        Visual.clear()
        colors = ['blue', 'red', 'green', 'orange', 'gold']
        for i in range(len(self.trucks)):
            Visual.plot_path(self.trucks[i].path, color = colors[i % len(colors)])

    def plot_missed(self):
        for truck in self.trucks:
            Visual.plot_customers(Depot(0,0), truck.path.missed_customers())

    def get_score(self):
        return score(self)

    # @TODO -- still lots to do here, of course ;)
    def get_children(self, big = True, medium = True, small = True, extra_big_move_children = False ):
        children = [] # list of states
        children_paths = []
        paths = self.paths
        n_customers = len( Distances.matrix[0] )
        trucks = self.trucks

        if big:
            #good
            #children_paths += State.shuffle( paths, 5 )
            #might be good or not, we've never used it
            #children_paths += State.alternating_shuffle_within_path( paths )
            children_paths += State.large_reconstruction( paths, 1000 if extra_big_move_children else 50 )
        if medium:
            if random.random() > 0.8:
                children_paths += State.random_nearest_neighbors(paths, 5, 10) #don't make n_touched bigger than 20 or else it won't work
                children_paths += State.use_clusters( paths, 10 )
                children_paths += State.move_central_customers_to_path_starts_and_ends( paths, n_customers // 5 )
        if small:
            # good
            # @TODO -- check that they are right
            # children_paths += State.wait_time_swap(paths)
            # children_paths += State.cargo_swap(paths, trucks)
            children_paths += State.time_swap(paths)

            children_paths += State.reverse(paths)

            children_paths += State.line_segment_insertion( paths, int( n_customers / 5 ), 10.0 )

            children_paths += State.fix_single_unreasonable( paths )

            children_paths += State.fix_group_unreasonable( paths )

            children_paths += State.switch_between_paths( paths, 20 )
            
            children_paths += State.missed_customer_time_swap (paths, 20)

            if random.random() > 0.8:
                children_paths += State.path_swap( paths, 20 )
        # child_paths should be a list containing three paths per entry (as a list)
        for child_paths in children_paths:
            trucks = []

            i = 1
            for child in child_paths:
                trucks.append(Truck(i, 0, 0, self.trucks[0].cargo, child))
                i += 1

            children.append(State(trucks, self))
        return children

    @staticmethod
    def move_central_customers_to_path_starts_and_ends( paths, n_children ):
        children = []
        nearest_neighbor_ids = sorted(range(1, 101), key = lambda cust: Distances.matrix[0][cust])[:n_children]

        for customer_id in nearest_neighbor_ids:
            path_number = 0
            for path_to_modify in paths:
                for index in [0, len(path_to_modify)]:
                    # first, copy the paths and get the customer from the path (pop out)
                    new_paths = copy.deepcopy( paths )
                    containing_path = State.find_path_containing_customer( new_paths, customer_id )
                    customer_index_in_path = containing_path.get_customer_index( customer_id )
                    customer = containing_path.route.pop( customer_index_in_path )

                    # now that we've got the customer, push it into position on the current path
                    path_to_insert_into = new_paths[path_number]
                    path_to_insert_into.route.insert( index, customer )

                    children.append( new_paths )

                path_number += 1

        return children

    @staticmethod
    def line_segment_insertion( paths, n_children, reasonable_distance ):
        children = []
        max_radius_to_keep = max(Distances().matrix[0]) / 8

        for k in range( n_children ):
            new_paths = copy.deepcopy( paths )

            # pick a path to look at
            path_a_index = randrange(len(paths))
            path_a = new_paths[path_a_index]
            # pick some customer on that path
            customer_a_index = randrange(len(path_a.route) - 1)
            customer_a = path_a.route[customer_a_index]
            x0, y0 = customer_a.x, customer_a.y

            second_break = False

            # go through every line segment on all paths and check if this one is close to that one
            for path in new_paths:
                points = [[0, 0]] + [[c.x, c.y] for c in path.route] + [[0, 0]]

                for j in range(0, len(points) - 1):
                    # x0, y0 = the point
                    # x1, y1 = the line end
                    # x2, y2 = the other line end
                    # px, py = the previous point in the path
                    # nx, ny = the next point in the path
                    x1, y1 = points[j][0], points[j][1]
                    x2, y2 = points[j+1][0], points[j+1][1]
                    px, py = path_a.route[customer_a_index-1].x, path_a.route[customer_a_index-1].y
                    nx, ny = path_a.route[customer_a_index+1].x, path_a.route[customer_a_index+1].y
                    try:
                        distance = abs( (y2-y1)*x0 + (x1-x2)*y0 + ( x1*y2 - x2*y1 ) )  / ( ( ( (y2-y1)**2 ) + ( (x1-x2)**2 ) )**0.5 )
                    except:
                        distance = 0 # divide by 0 == it's on the line == distance is 0
                    # make a chance if (a) the segment is close, (b) the next point is far, (c) the prior point is far
                    if distance <= reasonable_distance or ((px-x0)**2 + (py-y0)**2)**0.5 > max_radius_to_keep or ((nx-x0)**2 + (ny-y0)**2)**0.5 > max_radius_to_keep:
                        # hey, it's close to the line segment! remove the customer
                        # from it's original path and insert it after the customer at index j+1
                        path_a.route.remove( customer_a )
                        path.route.insert( j+1, customer_a )

                        children.append( new_paths )

                        # you're finished for this child; kill both of these for loops (allow third to continue)
                        second_break = True
                        break
                if second_break:
                    break

        return children

    @staticmethod
    def use_clusters( paths, n_children ):
        children = []

        for k in range( n_children ):
            new_paths = copy.deepcopy( paths )

            # get a customer to base the cluster on
            cluster_base_customer_id = choice( ClusterStore().clustered_customer_ids )
            # find the path that contains this customer
            containing_path = State.find_path_containing_customer( new_paths, cluster_base_customer_id )
            # separate out the paths aside from this one
            non_containing_paths = [path for path in new_paths if path != containing_path]
            # find the cluster which contains the chosen customer
            containing_cluster = ClusterStore.find_cluster_containing_customer( cluster_base_customer_id )

            # remove the other customers from whatever paths they are on
            customer_ids_to_handle = [c.number for c in containing_cluster.optimal_solution.route if c.number != cluster_base_customer_id]
            customers_to_handle = []
            indexes_for_removal = [[] for path in new_paths]


            # store the customers you'll have to handle
            # get the INDEXES of the customers you have to remove
            i = 0
            for path in new_paths:
                j = 0
                for customer in path.route:
                    if customer.number in customer_ids_to_handle:
                        indexes_for_removal[i].append(j)
                        customers_to_handle.append( customer )
                    j += 1
                i += 1

            # remove the customers at the desired indexes (backwards)
            i = 0
            for indexes in indexes_for_removal:
                for index in indexes[::-1]:
                    new_paths[i].route.pop( index )
                i += 1

            # force customers [in cyclical right order] into the solution
            id_to_insert_after = cluster_base_customer_id
            id_to_be_inserted = None
            for i in range( len( containing_cluster.optimal_solution ) - 1 ):
                id_to_be_inserted = containing_cluster.next_to_visit_ids( id_to_insert_after )
                containing_path.insert_customer( id_to_insert_after, id_to_be_inserted, customers_to_handle )
                id_to_insert_after = id_to_be_inserted

            children.append( new_paths )

        return children

    @staticmethod
    def reverse(paths):
        children = []
        for i in range(len(paths)):
            new_paths = copy.deepcopy(paths)
            new_paths[i].route.reverse()
            children.append(new_paths)
        return children

    @staticmethod #medium move
    # @TODO -- truck number dependency (entire function)
    def cycle(paths, times):
        children = []
        for i in range(15):
            route1 = paths[0].route
            route2 = paths[1].route
            route3 = paths[2].route
            length1 = len(route1)
            length2 = len(route2)
            length3 = len(route3)
            for i in range(0,times):
                rand1 = randint(0,length1-1)
                rand2 = randint(0,length2-1)
                rand3 = randint(0,length3-1)
                temp = route1[rand1]
                route1[rand1] = route2[rand2]
                route2[rand2] = route3[rand3]
                route3[rand3] = temp
            new_paths = [Path(route1), Path(route2), Path(route3)]
            children.append(new_paths)
            return children
    
            
    @staticmethod #small move
    def redistribute_more_evenly(paths):
        """ For ex, with 100 customers and 3 trucks, we expect 33 per truck.  Siphon off the
            surplus for any 'overloaded' paths and then add some surplus randomly into 'underloaded'
            paths """
        children = []

        expected = sum( [ len(element.route) for element in paths] ) / len(paths)
        overserved_paths = []
        underserved_paths = []
        surplus = 0

        for path in paths:
            if len( path.route ) > expected:
                overserved_paths.append( path )
                surplus += len( path.route ) - expected
            else:
                underserved_paths.append( path )

        # create 5 different moves
        for k in range(5):
            # create copies of the routes
            copy_overserved = [ copy.deepcopy(path.route) for path in overserved_paths ]
            copy_underserved = [ copy.deepcopy(path.route) for path in underserved_paths ]
            # move a total of [surplus] things from overserved routes to underserved routes
            for i in range(surplus):
                overserved_path = choice( copy_overserved )
                underserved_path = choice( copy_underserved )
                customer_to_move = overserved_path.pop( randrange( len ( overserved_path ) ) )
                underserved_path.insert( randrange( len( underserved_path ) ), customer_to_move )

            children.append([ Path( element ) for element in copy_underserved ] + [ Path( element ) for element in copy_overserved ])

        # a list containing lists-of-paths
        return children

    @staticmethod #big move
    def shuffle(paths, by_num):
        children = []

        for i in range(7):
            new_paths = []
            for path in paths:
                route = []
                for i in range(0, len(path.route), by_num - 1):
                    custs = path.route[i:i+by_num-1]
                    random.shuffle(custs, random.random)
                    for cust in custs:
                        route.append(cust)
                new_path = Path(route)

                new_paths.append(new_path)

            children.append(new_paths)

        return children

    @staticmethod #small move
    # check if swaps can make the paths valid if they weren't, tolerance controls added distance
    #this used to be get_fixed_children
    def sort_paths(paths):
        children = []

        pathnum = 0

        for path in paths:
            i = 0
            p = copy.deepcopy(path)
            prevtime = 0

            new_paths =  copy.deepcopy(paths)


            new_paths[pathnum] = Path(sorted(p.route, key = lambda customer: customer.close_time))

            is_sorted = True
            for i in range(min(len(new_paths[pathnum].route), len(p.route))):
                if not (new_paths[pathnum].route[i].x == p.route[i].x and new_paths[pathnum].route[i].y == p.route[i].y):
                    is_sorted = False

            if not is_sorted:
                children.append(new_paths)

            pathnum += 1

        return children

    @staticmethod #small move
    def path_swap(paths, n_children ):
        new_path_sets = []

        for i in range( n_children ):
            new_paths = copy.deepcopy( paths )
            # get two unique random paths
            path_a_index = randint(0, len(paths)-1)
            path_b_index = (path_a_index + randint(1, len(paths)-1)) % len(paths)
            path_a = new_paths[path_a_index]
            path_b = new_paths[path_b_index]
            # select two customers
            customer_a = randint(0, len(path_a.route) - 1)
            customer_b = randint(0, len(path_b.route) - 1)
            path_a.route[customer_a], path_b.route[customer_b] = path_b.route[customer_b], path_a.route[customer_a]
            new_path_sets.append(new_paths)

        return new_path_sets

    @staticmethod #small move
    def distance_swap(paths):
        children = []
        for i in range( 15 ):
            new_paths = [copy.deepcopy(element) for element in paths]
            path_index = randint(0, len(paths)-1)
            path = new_paths[path_index]
            # gets two random customers, if the first is farther then the secondthen swap
            customer_a = randint(0, len(path.route) - 1)
            customer_b = randint(customer_a, len(path.route) - 1)
            if Distances.get_distance(0, path.route[customer_a].number) > Distances.get_distance(0, path.route[customer_a].number):
                path.route[customer_a], path.route[customer_b] = path.route[customer_b], path.route[customer_a]
            children.append(new_paths)
        return children    
    
 #   @staticmethod #small move
 #   def cargo_swap(paths, trucks):
 #       children = []
 #       for i in range( 15 ):
 #           truck = trucks
 #           print (truck)
 #           new_paths = [copy.deepcopy(element) for element in paths]
 #           ipdb.set_trace()
 #           path_index = randint(0, len(paths)-1)
 #           #this gets two random paths that are not the same path. There is definitely a better way to to do this.
 #           #feel free to make this not suck
 #           path_a = new_paths[path_index]
 #           remaining_paths = new_paths.remove[path_a]
 #           path_b = randint(0, len(remaining_paths)-1)
 #           # gets two random customers, if the first is farther then the secondthen swap
 #           if (path_a.cargo_used > trucks.cargo):
 #               customer_a = randint(0, len(path_a.route) - 1)
 #               customer_b = randint(0, len(path_b.route) - 1)
 #               path.route[customer_a], path.route[customer_b] = path.route[customer_b], path.route[customer_a]
 #           children.append(new_paths)
 #       return children

    @staticmethod #medium move, 3 children
    def five_section_swap(paths):
        children = []
        for j in range(len(paths)):
            path = paths[j]
            new_route = copy.deepcopy(path.route)
            section_to_swap = []
            cs = []
            index = randint(0, len(new_route)-6)
            for i in range(index, index+5):
                section_to_swap.append(path.route[i])


                new_route.remove(new_route[i]) #@FIXME


                cs.append(path.route[i].number)

            for n in range(len(cs)-1):
                for a in range(len(new_route)-1):
                    if n == new_route[a].number:
                        new_route.remove(new_route[a])
                

            to_insert = randint(0, len(new_route) - 1)
            for k in range(to_insert, to_insert+5):
                new_route.insert(k, path.route[to_insert])

            new_paths = copy.deepcopy(paths)
            new_paths[j] = Path(new_route)
            children.append(new_paths)
        return children

    @staticmethod
    def fix_single_unreasonable( paths ):
        """If you travel an unreasonable distance at least to or from a customer,
            try moving it somewhere else closer???"""
        children = []
        threshold = max(Distances.matrix[0])/4.5

        path_number = 0
        for path in paths:
            # check depot to first customer
            if Distances.get_distance(0, path.route[0].number) > threshold or Distances.get_distance(path.route[0].number, path.route[1].number) > threshold:
                children += State.remove_and_insert_closer( 0, paths, path_number )
                
            # check all regular customers to e/o
            for i in range(0, len(path) - 2):
                if Distances.get_distance(path.route[i].number, path.route[i+1].number) > threshold or Distances.get_distance(path.route[i+1].number, path.route[i+2].number) > threshold:
                    children += State.remove_and_insert_closer( i+1, paths, path_number )

            # check last customer to depot
            if Distances.get_distance(path.route[-2].number, path.route[-1].number) > threshold or Distances.get_distance(path.route[-1].number, 0) > threshold:
                children += State.remove_and_insert_closer( -1, paths, path_number )

            path_number += 1

        return children

    @staticmethod
    def fix_group_unreasonable( paths ):
        """Suppose the distances in order are like [a]unreasonable[b]reasonable[c]reasonable[d]reasonable[e]unreasonable[f].
           Then move b, c, d, and e into a different path based on a near neighbor"""
        children = []
        threshold = max(Distances.matrix[0])/3.5
        path_number = 0
        for path in paths:
            # check depot to first customer
            if Distances.get_distance(0, path.route[0].number) > threshold:
                for j in range( 1, len(path) - 1 ):
                    if Distances.get_distance( path.route[j].number, path.route[j+1].number ) > threshold:
                        children += State.remove_and_insert_closer_as_group( 1, j, paths, path_number )
                
            # check all regular customers to e/o
            for i in range(0, len(path) - 1):
                if Distances.get_distance(path.route[i].number, path.route[i+1].number) > threshold:
                    for j in range( i + 1, len(path) - 1 ):
                        if Distances.get_distance( path.route[j].number, path.route[j+1].number ) > threshold:
                            children += State.remove_and_insert_closer_as_group( i+1, j, paths, path_number)

            path_number += 1
        return children

    @staticmethod
    def remove_and_insert_closer_as_group( first_removal_index, last_removal_index, paths, interesting_path_index ):
        children = []

        for i in range(1, 5):
            new_paths = copy.deepcopy(paths)
            path = new_paths[interesting_path_index]
            route = path.route
            customers_to_insert = []
            for k in range(first_removal_index, last_removal_index + 1):
                # the indexes will shift beneath our feet, so always remove at the same place
                customers_to_insert.append( route.pop(first_removal_index) )

            # range starts at 1 because 0 refers to itself and that's stupid and bad
            closest_customer_id = Distances.get_closest_customers( customers_to_insert[0] )[i]
            containing_path = State.find_path_containing_customer( new_paths, closest_customer_id )
            if containing_path:
                close_customer_index = containing_path.get_customer_index( closest_customer_id )
                for customer in customers_to_insert:
                    containing_path.route.insert( close_customer_index + 1, customer )
                    close_customer_index += 1
                children.append( new_paths )

        return children

    @staticmethod
    def remove_and_insert_closer( customer_index, paths, interesting_path_index ):
        children = []
        # find whoever is closest to it (should be four customers nearby-ish?)
        customer = paths[interesting_path_index].route[customer_index]
        closest_customers = Distances.get_closest_customers( customer )

        for customer_id in closest_customers[1:5]:
            # for each of those customer IDs, find the path where it is, and insert it
            # either before or after (50/50) the close customer
            new_paths = copy.deepcopy( paths )
            new_path = new_paths[interesting_path_index]
            customer = new_path.route.pop( customer_index )
            containing_path = State.find_path_containing_customer( new_paths, customer_id )

            if containing_path:
                close_customer_index = containing_path.get_customer_index( customer_id )
                if random.random() > 0.5:
                    containing_path.route.insert( close_customer_index + 1, customer )
                else:
                    containing_path.route.insert( close_customer_index, customer )
                children.append( new_paths )

        return children

    #works
    @staticmethod #medium move? , takes random set and does nearest neighbors on it
    def random_nearest_neighbors(paths, n_children, n_touched): #paths, number to do nearest neighbors on
        children = []
        n_touched = State.random_nn_limit(paths, n_touched)
        for k in range(n_children):
            new_paths = []
            for i in range(len(paths)):
                path = paths[i]
                new_path = copy.deepcopy(path.route)
                customers = [] #customers to do nearest neighbors
                r = random.randint(0, len(new_path) - n_touched)
                customers = copy.deepcopy(new_path[r:r + n_touched])
                for i in range(n_touched):
                    new_path.pop(r)

                customers = Dijsktra.get_nearest_neighbors(customers, customers[0])
                for x in range(0, n_touched):
                    new_path.insert(r+x, customers.route[x])

                new_paths.append(Path(new_path))
            children.append(new_paths)
        return children

    @staticmethod
    def random_nn_limit(paths, n_touched):
        lens = [len(path) for path in paths]
        if min(lens) < n_touched:
            return min(lens)
        else:
            return n_touched
            
    @staticmethod #large move
    def alternating_shuffle_within_path(paths):
        children = []

        for j in range(len(paths)):
            path = paths[j]
            temp_route = copy.deepcopy(path.route)
            new_route = []
            while(len(temp_route) > 0):
                cust = temp_route.pop(0)
                new_route.append(cust)
                temp_route = sorted(temp_route, key = lambda customer: Distances.get_distance( customer.number, cust.number ) )

            new_paths = copy.deepcopy(paths)
            new_paths[j] = Path(new_route)
            children.append(new_paths)

        return children

    @staticmethod
    def large_reconstruction(paths, n_children = 200, min_percentage = 25, max_percentage = 75 ):
        children = []
        n_customers = sum([len(path.route) for path in paths])
        customers = []
        for path in paths:
            for customer in path.route:
                customers.append(customer)
        n_paths = len(paths)

        for i in range( n_children ):
            new_paths = copy.deepcopy( paths )

            # choose a percentage between your min and max; multiply it and take it based on n_customers
            n_changes_to_make = int( n_customers * ( random.randint(min_percentage, max_percentage) / 100.0 ) )

            removed_customers = []
            for k in range( n_changes_to_make ):
                # remove #[n_changes_to_make] customers
                path_a = new_paths[ randint( 0, n_paths - 1 ) ]
                if len(path_a) > 1:
                    cust_a = path_a.route.pop( randrange( len( path_a.route ) ) )
                    removed_customers.append( cust_a )

            num_removed = len(removed_customers)

            while len(removed_customers) > 0:
                cust_a = removed_customers[0]
                closest_list = sorted(range(1, 101), key = lambda cust: Distances.matrix[cust_a.number][cust])
                closest_list = [element for element in closest_list if element not in map(lambda c: c.number, removed_customers)][:3]
                closest = choice( closest_list )
                removed_customers.remove(cust_a)
                for path in new_paths:
                    closest_index = path.get_customer_index(closest)
                    if closest_index != -1:
                        path.route.insert(closest_index, cust_a)

            if sum( [len(path) for path in new_paths] ) == n_customers:
                children.append( new_paths )

        return children

    @staticmethod
    def switch_between_paths(paths, numtoswap):
        new_path_lists = []

        for i in range(numtoswap):
            p = copy.deepcopy(paths)

            path_a = randint(0, len(paths)-1)
            path_b = randint(0, len(paths)-1)

            cust_a = randint(0, len(p[path_a].route) - 1)
            cust_b = randint(0, len(p[path_b].route) - 1)

            temp = p[path_a].route[cust_a]
            p[path_a].route[cust_a] = p[path_b].route[cust_b]
            p[path_b].route[cust_b] = temp

            new_path_lists.append( p )

        return new_path_lists

    @staticmethod
    def find_path_containing_customer(paths, customer_id):
        for path in paths:
            for customer in path.route:
                if customer.number == customer_id:
                    return path

    @staticmethod
    ## Swaps late
    def time_swap (paths, n_children = 15):
        children = []
        for i in range( n_children ):
            new_paths = copy.deepcopy(paths)
            path = new_paths[randrange( len( paths ) ) ]
            # gets two random customers, if the first is farther then the secondthen swap
            index_a = randrange( len( path ) )
            index_b = randrange( len( path ) )
            customer1 = path.route[ index_a ]
            customer2 = path.route[ index_b ]
            ## WE CAN ALSO DO THIS BASED ON SERVICE TIMES

            if (index_a < index_b and customer1.close_time > customer2.close_time):
                ## if the closing time of cust1 is later than that of cust2, swap 1 and 2
                path.route[index_a], path.route[index_b] = path.route[index_b], path.route[index_a]
            elif (index_a > index_b and customer1.close_time < customer2.close_time):
                path.route[index_a], path.route[index_b] = path.route[index_b], path.route[index_a]
            children.append(new_paths)

        return children

    @staticmethod
    def missed_customer_time_swap(paths, n_children):
        children = []
        for n in range(n_children):
            new_paths = []
            for path in paths:
                new_path = copy.deepcopy(path)
                missed_customers = new_path.missed_customers()
                if missed_customers: #if there are missed customers
                    r = randint(0, len(missed_customers) - 1) #pick a missed customer
                    c,t = missed_customers[r], missed_customers[r].close_time
                    for x in range(0, new_path.route.index(c)): #look through the customers before the missed customer since it should be earlier
                        if new_path.get_arrival_time_of_customer(new_path.route[x]) < t: #find a spot in the path before the close time
                            new_path.route.remove(c)
                            new_path.route.insert(x-1, c)
                            new_paths.append(new_path)
            children.append(new_paths)
        return children
            
    @staticmethod
    def fix_inter_path_intersections(paths):
        children = []
        for i in range(len(paths)):
            for j in range(i, len(paths)):
                new_paths = copy.deepcopy(paths)
                intersections = new_paths[i].intersects_with_other(new_paths[j])

                if len(intersections) > 0:
                    k = randint(0,len(intersections)-1)
                    points = intersections[k]
                    cust1 = points[randint(0,1)]
                    cust2 = points[randint(2,3)]
                    if not(cust1 == None or cust2 == None):
                        index1 = new_paths[i].route.index(cust1)
                        index2 = new_paths[j].route.index(cust2)
                        new_paths[i].route[index1] = cust2
                        new_paths[j].route[index2] = cust1

                    children.append(new_paths)
        return children

    def __repr__(self):
        str = "\n<State: "
        for i in range(len(self.trucks)):
            str += "Truck {0}: {1}".format(i, self.trucks[i].path.route)
        str += ">"
        return str



"""

    ## helper method for wait_time_swap
    def get_closest_customer (filename, customer):
        with open(path + filename) as f:
        customers = import_customers(filename.split("_")[0] + ".txt", False)
        lines = f.readlines()

        ids = []
        for line in lines[5:]:
            ids.append(line.split()[3:])

    @staticmethod
    ## if the truck is being a little shit and waiting too long, change the path to include another customer in the meantime
    def wait_time_swap (paths, n_children = 15):
        children = []
        for i in range (n_children):
            customers = []
            new_paths = copy.deepcopy(paths)
            path = new_paths[i]

            wait_time = 0
            prev_customer = path.route[0]
            time = Distances.get_distance(prev_customer.number, 0)

            if time < prev_customer.open_time:
             wait_time += prev_customer.open_time - time
             time = prev_customer.open_time

            time += prev_customer.service_time

            for c in path.route:

                time += Distances.get_distance(prev_customer.number, c.number)
                prev_customer = c

                if time < c.open_time:
                    wait_time += prev_customer.open_time - time
                    time = c.open_time

                ## wait time is arbitrarily picked, can change
                if wait_time > 20:
                    customers = get_closest_customer(c)
                    ## generates nearest customers
                    for x in customers:
                        ## if the truck has to wait long at some new customers too, forget em
                        ## time+5 can be changed
                        if (time+5) < x.open_time:
                            customers = customers.remove(x)
                        else:
                            pass
                time += c.service_time
                if len (customers) != 0:
                    ##choose the first customer (cause it doesn't really matter) as the add-in
                    replacement_customer = customers.pop(0)
                    ## adds replacement customer into path.route
                    path.route.append(replacement_customer)

                children.append(new_paths)

        return children

"""


