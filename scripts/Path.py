# Jahnik and Dan
# Simple class to interact with a route/path of a truck
# Can return the total distance, customer at a certain time ..
# c was used as customer in order to avoid conflict with old code

import math

class Path():

    def __init__(self, route):
        self.route = route #list of customers
        # @TODO -- now that i think abou tit, we should probably store
        # self.distance on here as well.  otherwise, we're going to be doing a lot of
        # repeated calculations when we could just be accessing a value

    # returns the total distance
    def get_distance(self):
        distance = 0
        prev_customer = None
        is_first_time = True

        # @TODO -- this if/else seems a little suspect to me... shouldn't we just
        # add the depot distance once and ignore the first customer or something?
        for c in self.route:
            if is_first_time:
                distance += ((c.x)**2 + (c.y)**2)**.5
                prev_customer = c
                is_first_time = False
            else:
                distance += ((c.x-prev_customer.x)**2 + (c.y-prev_customer.y)**2)**.5
                prev_customer = c

        distance += (prev_customer.x**2 + prev_customer.y**2)**.5

        return distance

    def get_arrival_time_of_customer(self, cust):
        """Returns the time at which the truck on this path arrives at this customer
        given the order of customers prior to the given customer and their windows"""

        prev_customer = None
        time = 0
        is_first_time = True

        for c in self.route:
            if is_first_time:
                # truck leaves from (0, 0)
                time = math.hypot(c.x, c.y)
                prev_customer = c

                is_first_time = False
            else:
                time += ((c.x-prev_customer.x)**2 + (c.y-prev_customer.y)**2)**.5
                prev_customer = c


            # if truck arrives before customer is open, assume truck waits
            if time < c.open_time:
                time = c.open_time

            if (c == cust):
                return time

            time += c.service_time

        return -1

    def is_valid(self):
        # @TODO -- just a note: comments before a function aren't "part of python" in any really meaningful ways.
        # if you do it like this -- called a docstring -- then you can actually access this information while you're
        # using a python interpreter and such, which can be very convenient.
        #
        # you don't need to do anything here; just a note for the future
        """returns whether the truck makes it on time to every customer by returning
        an array of the customers missed. If the path is valid, an empty array will be returned"""

        prev_customer = None
        time = 0
        is_first_time = True
        missedCustomers = []

        for c in self.route:
            # @TODO -- again, this feels a little suspect to me.  maybe just add the depot and ignore
            # the first customer in the list.  otherwise we have to evaluate an if/else every time
            if is_first_time:
                # truck leaves from (0, 0)
                time = math.hypot(c.x, c.y)
                prev_customer = c

                is_first_time = False
            else:
                time += ((c.x-prev_customer.x)**2 + (c.y-prev_customer.y)**2)**.5
                prev_customer = c

            # if truck arrives before customer is open, assume truck waitds
            if time < c.open_time:
                time = c.open_time

            # if truck arrives late, add to missedCustomers
            if time > c.close_time:
                missedCustomers.append(c)

            time += c.service_time

        # @TODO -- the name is_valid makes me expect this would return at least a boolean value
        # [and perhaps something else in addition]
        # maybe we should return True/False, missedCustomers instead?
        return missedCustomers

    # gets the customer the truck was last at
    def get_last_customer_visited(self, current_time):
        prev_customer = None
        is_first_time = True
        time = 0

        for c in self.route:
            # @TODO -- again, suspicious about the first time thing here.  you can really see why now;
            # it's forcing the duplication of a lot of code.
            if is_first_time:

                # truck leaves from (0, 0)
                time = math.hypot(c.x, c.y)
                if(time > current_time):
                    return None

                # if truck arrives before customer is open, assume truck waits
                if time < c.open_time:
                    time = c.open_time
                time += c.service_time

                if(time > current_time):
                    return c

                prev_customer = c
                is_first_time = False
            else:
                time += ((c.x - prev_customer.x) ** 2 + (c.y - prev_customer.y) ** 2) ** .5

                if(time > current_time):
                    return prev_customer

                # if truck arrives before customer is open, assume truck waitds
                if time < c.open_time:
                    time = c.open_time
                time += c.service_time

                if(time > current_time):
                    return c

                prev_customer = c

    # returns whether the path intersects itself
    def intersects_self(self):
        # @TODO -- i know we stole this from stackoverflow, but have we tested it?
        # let's make sure we do that [and then delete this comment]
        intersects = False
        points = [(0, 0)]
        for c in self.route:
            points.append((c.x, c.y))

        for i in range(1, len(points)):
            for j in range(i + 1, len(self.route)):
                if (Path.lines_intersect(points[i - 1], points[i], points[j], points[j - 1])):
                    intersects = True

        return intersects

    # Will probably be used for inserting in completed solutions for clusters
    def append(self, toAppend):
        self.route.append(toAppend.route)

    # Will probably be used for inserting in completed solutions for clusters
    def insert(self, toAppend, index):
        for c in toAppend.route:
            self.insert(index, c)
            index += 1


    # Given two lines AB and CD, determines if they intersect
    # If
    # source http://bryceboe.com/2006/10/23/line-segment-intersection-algorithm/
    @staticmethod
    def lines_intersect(A, B, C, D):
        return Path.ccw(A,C,D) != Path.ccw(B,C,D) and Path.ccw(A,B,C) != Path.ccw(A,B,D)

    # helper method for lines_intersect()
    @staticmethod
    def ccw(A, B, C):
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
            return self.route[index]
        else:
            return None

    def distance_to_next(self, customer):
        index = self.route.index(customer) + 1
        if index < len(self.route):
            return self.route[index]
        else:
            return None

    def __repr__(self):
        return "<Path: {0}>".format(self.route)