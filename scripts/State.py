from Visual import Visual
from Truck import Truck
import copy
from HeuristicScore import score
from Dijkstra import Dijsktra
from Path import Path
from Depot import Depot
from ClusterStore import ClusterStore
from random import randint, randrange, choice
from Distances import Distances
from Customer import Customer
import random
try:
    import ipdb
except:
    print "Skipping ipdb import because Dan's school is full of jerks"

class State():

    def __init__(self, trucks, parent = None):

        self.trucks = trucks
        self.paths = [truck.path for truck in trucks]

        self.distance = None
        self.parent = parent

        #  @TODO -- update get_children sub-methods to include parent
        #  @TODO -- should we also maintain children...?

        #  @TODO -- similar to reason above:  maintain score(?)

    def calculate_distance(self):
        self.distance = 0
        for truck in self.trucks:
            self.distance += truck.path.calculate_distance()
        return self.distance

    def plot(self):
        colors = ['g', 'c', 'm', 'b', 'y', 'r']
        for i in range(len(self.trucks)):
            Visual.plot_path(self.trucks[i].path, color = colors[i % len(colors)])
        Visual.show()

    def plot_missed(self):
        for truck in self.trucks:
            Visual.plot_customers(Depot(0,0), truck.path.missed_customers())
        Visual.show()

    def get_score(self):
        return score(self)

    # @TODO -- still lots to do here, of course ;)
    def get_children(self, big = True, medium = True, small = True, extra_big_move_children = False ):
        children = [] # list of states
        children_paths = []
        paths = self.paths

        if big:
            #good
            #children_paths += State.shuffle( paths, 5 )
            #might be good or not, we've never used it
            #children_paths += State.alternating_shuffle_within_path( paths )
            #children_paths += State.large_reconstruction( paths, 1000 if extra_big_move_children else 200 )
            pass
        if medium:
            #not that good
            #children_paths += State.cycle(paths, 4)
            #might be good, never used
            #children_paths += State.five_section_swap(paths)
            #children_paths += State.random_nearest_neighbors(paths)
            
            # @DEBUG
            pass
            #children_paths += State.use_clusters( paths, 10 )
        if small:
            #not that good
            #children_paths += State.redistribute_more_evenly(paths)
            #good
       
            children_paths += State.time_swap(paths)
            children_paths += State.reverse(paths)
            children_paths += State.fix_intersections(paths)
            children_paths += State.fix_inter_path_intersections(paths)
            children_paths += State.sort_paths( paths )
            #children_paths += State.path_swap( paths, 15 )
            #children_paths += State.distance_swap( paths )
            children_paths += State.switch_between_paths( paths, 100 )
            #children_paths += State.swap_neighbors( paths )
            children_paths += State.move_customer( paths, 8 )
        # child_paths should be a list containing three paths per entry (as a list)
        for child_paths in children_paths:
            trucks = []

            i = 1
            for child in child_paths:
                trucks.append(Truck(i, 0, 0, 700, child))
                i += 1

            children.append(State(trucks, self))
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

    @staticmethod
    def fix_intersections(paths):
        children = []
        for i in range(len(paths)):
            new_paths = copy.deepcopy(paths)
            path = new_paths[i]
            intersections = path.intersects_self()
            if(len(intersections) > 0):
                k = randint(0, len(intersections) - 1)
                intersection = intersections[k]
                i1 = path.route.index(intersection[1])
                i2 = path.route.index(intersection[2])
                path.route[i1], path.route[i2] = path.route[i2], path.route[i1]
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
    
    @staticmethod
    def move_customer(paths, numtimes):
        children = []
        new_paths = copy.deepcopy(paths)
        for i in range(numtimes):
            rp = randint(0, len(paths)-1)
            path = new_paths[rp]
            rstart = randint(0, len(path)-1)
            rend = randint(0, len(path)-2)
            while rend == rstart:
                rend = randint(0, len(path))
                
            c = path.route[rstart]
            path.route.pop(path.route.index(path.route[rstart]))
            path.route.insert(rend, c)
        
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

    @staticmethod #medium move, 3 children
    def five_section_swap(paths):
        children = []
        for j in range(len(paths)):
            path = paths[j]
            new_route = copy.deepcopy(path.route)
            section_to_swap = []
            index = randint(0, len(path)-6)
            for i in range(index, index+5):
                section_to_swap.append(path.route[i])
                new_route.remove(new_route[i]) #@FIXME

            to_insert = randint(0, len(new_route) - 1)
            for k in range(to_insert, to_insert+5):
                new_route.insert(k, path.route[to_insert])

            new_paths = copy.deepcopy(paths)
            new_paths[j] = Path(new_route)
            children.append(new_paths)
        return children

    #@FIXME
    @staticmethod #medium move? , takes random set of 10 and does nearest neighbors on it
    def random_nearest_neighbors(paths):
        children = []
        new_paths = []
        for i in range(len(paths)):
            path = paths[i]
            new_path = copy.deepcopy(path.route)
            customers = [] #customers to do nearest neighbors
            r = random.randint(0, len(path.route) - 10)
            for l in range(r, r+10):
                customers.append(new_path[l])
            customers = Dijsktra.get_nearest_neighbors(customers, customers[0])
            #print customers
            for x in range(r, r+10):
                #print x-r
                #print customers[0]
                new_path[x] = customers.route[x - r]
            new_paths.append(new_path)
    
        children.append(new_paths)
        return children
            

        
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
        n_paths = len(paths)

        for i in range( n_children ):
            new_paths = copy.deepcopy( paths )

            # choose a percentage between your min and max; multiply it and take it based on n_customers
            n_changes_to_make = int( n_customers * ( random.randint(min_percentage, max_percentage) / 100.0 ) )

            removed_customers = []
            for k in range( n_changes_to_make ):
                # remove #[n_changes_to_make] customers
                path_a = new_paths[ randint( 0, n_paths - 1 ) ]
                if len(path_a) > 0:
                    cust_a = path_a.route.pop( randint( 0, len( path_a.route ) - 1 ) )
                    removed_customers.append( cust_a )

            for cust_a in removed_customers:
                path_a = new_paths[ randint( 0, n_paths - 1 ) ]
                if len(path_a) > 0:
                    path_a.route.insert( randrange( len(path_a.route) ), cust_a )
                else:
                    path_a.route.insert( 0, cust_a )

            children.append( new_paths )

        return children
    
    @staticmethod
    def swap_neighbors(paths):
        children = []
        new_paths = []
        for path in paths:
            new_path = []
            new_path = copy.deepcopy(path)
            r = randint(0, len(new_path.route) - 2)
            neighbor = new_path.route[r]
            new_path.route[r] = new_path.route[r+1]
            new_path.route[r+1] = neighbor
            new_paths.append(new_path)
        
        children.append(new_paths)
        
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
    def fix_inter_path_intersections(paths):
        children = []
        for i in range(len(paths)):
            for j in range(i+1, len(paths)):
                new_paths = copy.deepcopy(paths)
                intersections = new_paths[i].intersects_with_other(new_paths[j])

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
