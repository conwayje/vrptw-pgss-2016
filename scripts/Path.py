# Jahnik and Dan
# Simple class to interact with a route/path of a truck
# Can return the total distance, customer at a certain time ..
# c was used as customer in order to avoid conflict with old code

import math
from Distances import Distances
from Customer import Customer
try:
    import ipdb
except:
    print "Skipping ipdb import because Dan's school is full of jerks"

class Path():

    def __init__(self, route):
        self.route = route # list of customers
        self.distance = self.calculate_distance()
        self.intersecting_segments = []

    def __len__(self):
        return len( self.route )

    def calculate_distance(self):
        """Returns the total distance in the route"""

        if len( self ) == 0:
            return 0

        prev_customer = self.route[0]
        distance = Distances.get_distance(0, prev_customer.number)

        for c in self.route[1:]:
            distance += Distances.get_distance(prev_customer.number, c.number)
            prev_customer = c

        distance += Distances.get_distance(prev_customer.number, 0)

        return distance

    def get_arrival_time_of_customer(self, cust):
        """Returns the time at which the truck on this path arrives at this customer
        given the order of customers prior to the given customer and their windows"""

        prev_customer = self.route[0]
        time = Distances.get_distance(prev_customer.number, 0)

        if time < prev_customer.open_time:
            time = prev_customer.open_time

        if prev_customer == cust:
            return time

        time += prev_customer.service_time

        for c in self.route[1:]:

            time += Distances.get_distance(prev_customer.number, c.number)
            prev_customer = c

            # if truck arrives before customer is open, assume truck waits
            if time < c.open_time:
                time = c.open_time

            if (c == cust):
                return time

            time += c.service_time

        return -1

    def missed_customers(self):
        """Formerly isValid().  Returns whether the truck makes it on time to every customer by returning
        an array of the customers missed. If the path is valid, an empty array will be returned"""

        if len( self ) == 0:
            return []

        prev_customer = self.route[0]
        time = Distances.get_distance(prev_customer.number,0)

        missedCustomers = []

        # if truck arrives before customer is open, assume truck waits
        if time < prev_customer.open_time:
            time = prev_customer.open_time

        # if truck arrives late, add to missedCustomers
        if time > prev_customer.close_time:
            missedCustomers.append(prev_customer)

        time += prev_customer.service_time

        for c in self.route[1:]:
            time += Distances.get_distance(prev_customer.number, c.number)
            prev_customer = c

            # if truck arrives before customer is open, assume truck waits
            if time < c.open_time:
                time = c.open_time

            # if truck arrives late, add to missedCustomers
            if time > c.close_time:
                missedCustomers.append(c)

            time += c.service_time

        return missedCustomers

    def get_last_customer_visited(self, current_time):
        """Gets the customer the truck was last at"""
        prev_customer = self.route[0]

        time = Distances.get_distance(prev_customer.number, 0)
        if (time > current_time):
            return None

        # if truck arrives before customer is open, assume truck waits
        if time < prev_customer.open_time:
            time = prev_customer.open_time
        time += prev_customer.service_time

        if (time > current_time):
            return prev_customer

        for c in self.route[1:]:

            time += Distances.get_distance(prev_customer.number, c.number)

            if(time > current_time):
                return prev_customer

            # if truck arrives before customer is open, assume truck waitds
            if time < c.open_time:
                time = c.open_time
            time += c.service_time

            if(time > current_time):
                return c

            prev_customer = c
        return None

    def intersects_self(self):
        """Returns where the path intersects itself"""
        intersecting_segments = []
        points = [(None, 0, 0)]

        for c in self.route:
            points.append((c, c.x, c.y))

        points.append((None, 0, 0))

        for i in range(0, len(points) - 2):
            for j in range(i + 2, len(points) - 1 ):
                if (Path.lines_intersect(points[i], points[i+1], points[j], points[j+1])):
                    intersecting_segments.append([points[i][0], points[i+1][0], points[j][0], points[j+1][0]])

        # save the intersecting segments on the instance
        self.intersecting_segments = intersecting_segments

        return intersecting_segments

    def number_intersections(self):
        return len( self.intersecting_segments )

    # Will probably be used for inserting in completed solutions for clusters
    def append(self, toAppend):
        self.route.append(toAppend.route)

    # Will probably be used for inserting in completed solutions for clusters
    def lol_insert(self, toAppend, index):
        for c in toAppend.route:
            self.insert(index, c)
            index += 1

    # Credit: http://bryceboe.com/2006/10/23/line-segment-intersection-algorithm/
    @staticmethod
    def lines_intersect(A, B, C, D):
        """Given two lines AB and CD, determines if they intersect"""
        return Path.ccw(A,C,D) != Path.ccw(B,C,D) and Path.ccw(A,B,C) != Path.ccw(A,B,D)

    @staticmethod
    def ccw(A, B, C):
        """Helper method for lines_intersect()"""
        # @TODO -- there's a liiiiittle bit too much magic happening here.  so what is
        # "A" exactly, and what does the assignment do?
        #
        # might want to add a docstring describing the structure of the arguments; it's not
        # immediately obvious what it's expecting
        (Ac, Ax, Ay) = A
        (Bc, Bx, By) = B
        (Cc, Cx, Cy) = C
        return (Cy - Ay) * (Bx - Ax) > (By - Ay) * (Cx - Ax)

    def distance_to_previous(self, customer):
        index = self.route.index(customer) - 1
        if index >= 0:
            return Distances.get_distance(customer.number, self.route[index].number)
        else:
            return Distances.get_distance(customer.number, 0)

    def distance_to_next(self, customer):
        index = self.route.index(customer) + 1
        if index < len(self.route):
            return Distances.get_distance(customer.number, self.route[index].number)
        else:
            return Distances.get_distance(customer.number, 0)

    def cargo_used(self, customer=None):
        result = 0
        for cust in self.route:
            result += customer.demand
            if customer == cust:
                return result
        return result

    def number_missed_by_time(self):
        return len(self.missed_customers())

    #@TODO -- Please check... was always return 0 before
    def number_missed_by_cargo(self, cargo):
        '''Return the number of customers missed by cargo'''
        index = 0
        cargo_used = 0
        for cust in self.route:
            cargo_used += cust.demand
            if cargo_used > cargo:
                return len(self.route) - index
            index += 1
        return 0

    def customer_ids(self):
        """Returns a *SET* of customer IDs based on the route of this path.

           Note that sets are faster at returning in/out than lists, though
           other operations are impossible or worse =)
        """
        return {customer.number for customer in self.route}

    def get_wait_time(self):
        if len( self ) == 0:
            return 0

        wait_time = 0
        prev_customer = self.route[0]
        time = Distances.get_distance(prev_customer.number, 0)

        if time < prev_customer.open_time:
            wait_time += prev_customer.open_time - time
            time = prev_customer.open_time

        time += prev_customer.service_time

        for c in self.route[1:]:

            time += Distances.get_distance(prev_customer.number, c.number)
            prev_customer = c

            # if truck arrives before customer is open, assume truck waits
            if time < c.open_time:
                wait_time += prev_customer.open_time - time
                time = c.open_time

            time += c.service_time

        return wait_time

    def intersects_with_other(self, path):
        points_1 = [(None, 0, 0)]
        points_2 = [(None, 0, 0)]
        for c in self.route:
            points_1.append((c, c.x, c.y))
        for c in path.route:
            points_2.append((c, c.x, c.y))
        points_1.append((None, 0,0))
        points_2.append((None, 0,0))

        intersecting_segments = []
        for i in range(len(points_1)-1):
            for j in range(len(points_2) - 1):
                if Path.lines_intersect(points_1[i], points_1[i+1], points_2[j], points_2[j+1]):
                    intersecting_segments.append([points_1[i][0], points_1[i+1][0], points_2[j][0], points_2[j+1][0]])
        return intersecting_segments

    ## Calculates number of times the truck waits for a hella long time
    def get_number_of_excessive_waits(self):
        num_waits = 0

        if len( self ) == 0:
            return 0

        wait_time = 0
        prev_customer = self.route[0]
        time = Distances.get_distance(prev_customer.number, 0)

        if time < prev_customer.open_time:
            wait_time += prev_customer.open_time - time
            time = prev_customer.open_time

        time += prev_customer.service_time

        for c in self.route[1:]:

            time += Distances.get_distance(prev_customer.number, c.number)
            prev_customer = c

            if time < c.open_time:
                wait_time += prev_customer.open_time - time
                time = c.open_time
            ######## THE WAIT TIME VALUE IS ARBITRARILY PICKED, CAN CHANGE IF NECESSARY
            if wait_time > 20:
                num_waits += 1

            time += c.service_time
        
        return num_waits

    def num_unreasonable_distances(self):
        threshhold = max(Distances.matrix[0])/3.5
        num = 0

        prev_customer = self.route[0]
        distance = Distances.get_distance(0, prev_customer.number)

        if distance > threshhold:
            num += 1

        for c in self.route[1:]:
            if(Distances.get_distance(prev_customer.number, c.number) > threshhold):
                num += 1
            prev_customer = c
        return num

    def insert_customer( self, anchor_id, inserted_id, customer_list ):
        """ Args: ( ID of a customer; ID of a customer to be inserted onto the path after anchor; list of customers to choose from )"""
        anchor_index = self.get_customer_index( anchor_id )
        customer = filter( lambda c: c.number == inserted_id, customer_list )[0]
        self.route.insert( anchor_index + 1, customer )

    def get_customer_index( self, customer_id ):
        """ Finds the customer's index in the path's route given a customer's ID """
        for c in range(len(self.route)):
            if self.route[c].number == customer_id:
                return c
        return -1

    def __repr__(self):
        # return "<Path: {0}>".format(self.route)
        return "<Path: {}>".format([customer.number for customer in self.route])

