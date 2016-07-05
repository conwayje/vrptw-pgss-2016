from copy import deepcopy

class Truck():
  def __init__(self, id_number, ordered_customers, current_customer_number = None):
    self.id_number = id_number
    self.ordered_customers = ordered_customers
    self.current_customer_number = 0

  def __str__(self):
    return "<Truck #{}: ({})>".format(self.id_number, self.ordered_customers)

  def get_total_route_distance(self, distance_matrix, depot):
    route_distance = 0
    initial_distance = Truck.get_quick_distance(depot, self.ordered_customers[0], distance_matrix)
    route_distance += initial_distance
    for i in range(len(self.ordered_customers) - 1):
      route_distance += Truck.get_quick_distance(self.ordered_customers[i], self.ordered_customers[i + 1], distance_matrix)
    final_distance = Truck.get_quick_distance(self.ordered_customers[-1], depot, distance_matrix)
    route_distance += final_distance
    return route_distance

  @staticmethod
  def get_quick_distance(location_a, location_b, distance_matrix):
    return distance_matrix[location_a.id_number][location_b.id_number]


  def get_used_capacity(self):
    return sum([customer.amount for customer in self.ordered_customers])

  def add_last_customer_visit(self, customer):
    self.ordered_customers.append( customer )
    self.current_customer_number = customer.id_number

  def get_closest_allowed_neighbor(self, distance_matrix, customers, vehicle_capacity):
    # does NOT include the depot as a possibility
    found = False
    current_position = self.current_customer_number
    neighbors_copy = deepcopy( distance_matrix[current_position] )
    while( not found ):
      try:
        nearest_remaining_neighbor_distance = min([element for element in neighbors_copy[1:] if element != None and element != 0])
        nearest_remaining_neighbor_number = neighbors_copy.index(nearest_remaining_neighbor_distance)
        nearest_remaining_customer = customers[nearest_remaining_neighbor_number]
        if nearest_remaining_customer.is_serviced == False and \
            nearest_remaining_customer.amount < vehicle_capacity - self.get_used_capacity() and \
            nearest_remaining_customer.is_depot == False:
          nearest_remaining_customer.is_serviced = True
          found = True
          return nearest_remaining_customer
        else:
          neighbors_copy[nearest_remaining_neighbor_number] = None
      except ValueError:
        return None
