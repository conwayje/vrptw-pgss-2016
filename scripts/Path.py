# Jahnik and Dan
# Simple class to interact with a route/path of a truck
# Can return the total distance, customer at a certain time ..
# c was used as customer in order to avoid conflict with old code

import math
from Distances import Distances

class Path():

    def __init__(self, route):
        self.route = route # list of customers
        self.distance = self.calculate_distance()

    def __len__(self):
        return len( self.route )

    def calculate_distance(self):
        """Returns the total distance in the route"""

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
        """Returns whether the path intersects itself"""
        intersects = 0
        points = [(0, 0)]
        for c in self.route:
            points.append((c.x, c.y))

        points.append((0,0))

        for i in range(1, len(points)):
            for j in range(i + 1, len(self.route)):
                if (Path.lines_intersect(points[i - 1], points[i], points[j], points[j - 1])):
                    intersects += 1

        return intersects

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
        (Ax, Ay) = A
        (Bx, By) = B
        (Cx, Cy) = C
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

    #@TODO -- Please check... was always return 0 before
    def get_index_customer_missed(self, cargo):
        '''Return the index of the first customer missed, will return -1 if makes it'''
        index = 0
        cargo_used = 0
        for cust in self.route:
            cargo_used += cust.demand
            if cargo_used > cargo:
                return index
            index += 1
        return -1

    def customer_ids(self):
        """Returns a *SET* of customer IDs based on the route of this path.

           Note that sets are faster at returning in/out than lists, though
           other operations are impossible or worse =)
        """
        return {customer.number for customer in self.route}


    def get_wait_time(self):
        wait_time = 0
        prev_customer = self.route[0]
        time = Distances.get_distance(prev_customer.number, 0)

        if time < prev_customer.open_time:
            wait_time += prev_customer.open_time - time
            time = prev_customer.open_time


        for c in self.route[1:]:

            time += Distances.get_distance(prev_customer.number, c.number)
            prev_customer = c

            # if truck arrives before customer is open, assume truck waits
            if time < c.open_time:
                wait_time += prev_customer.open_time - time
                time = c.open_time

            time += c.service_time

        return wait_time

    def insert_customer( self, anchor_id, inserted_id, customer_list ):
        """ Args: ( ID of a customer; ID of a customer to be inserted onto the path after anchor; list of customers to choose from )"""
        anchor_index = self.get_customer_index( anchor_id )
        customer = filter( lambda c: c.number == inserted_id, customer_list )[0]
        self.route.insert( anchor_index + 1, customer )

    def get_customer_index( self, customer_id ):
        """ Finds the customer's index in the path's route given a customer's ID """
        return self.route.index( filter( lambda c: c.number == customer_id, self.route )[0] )

    def __repr__(self):
        # return "<Path: {0}>".format(self.route)
        return "<Path: {}>".format([customer.number for customer in self.route])

