import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy
import ipdb
from truck import Truck
from customer import Customer

FILE_NAME = "C2_2_8.TXT"
customers = []
trucks = []
depot = None
maximum_allowed_vehicles = 6
vehicle_capacity = 700
QUINTIQ_DISTANCE = 1820.53
total_score = 999999999
distance_matrix = [[0] * 10 for x in range(10)] # 10 is just a stupid magic number to start


def main():
  initialize_customers_and_depot()
  initialize_trucks()
  initialize_distance_matrix()
  initial_solution = get_initial_solution()
  adjust_number_of_trucks()
  show_plot()
  calculate_and_show_current_score()
  for x in range(6):
    plot_for_truck(x)

  plt.show()

def plot_for_truck(k):
  global depot, customers
  n = len(customers)
  x = [element.x for element in customers[1:]]
  y = [element.y for element in customers[1:]]
  plt.scatter(x, y)
  plt.scatter(depot.x, depot.y, c="r")


  truck = trucks[k]
  x2 = []
  y2 = []

  x2.append( depot.x )
  y2.append( depot.y )
  cs = truck.ordered_customers
  for c in cs:
    x2.append( c.x )
    y2.append( c.y )

  x2.append( depot.x )
  y2.append( depot.y )

  colors = ["b","g","r","c","m","k"]

  ipdb.set_trace()

  plt.plot(x2, y2, c=colors[k], linewidth=3)

  # plt.show()

def calculate_and_show_current_score():
  global total_score
  score_sum = calculate_total_score()
  show_current_score(score_sum)

def show_current_score(score):
  print "Current score: {}".format(score)

def calculate_total_score():
  global distance_matrix, depot
  scores = [truck.get_total_route_distance(distance_matrix, depot) for truck in trucks]
  score_sum = sum(scores)
  return score_sum

def print_all_truck_contents():
  print "Printing ID Numbers"
  for truck in trucks:
    print "Truck #{}: ".format(truck.id_number),
    for customer in truck.ordered_customers:
      print "{} ".format(customer.id_number),
    print ""

def adjust_number_of_trucks():
  global maximum_allowed_vehicles, trucks
  non_empty_trucks = [truck for truck in trucks if truck.ordered_customers != []]
  maximum_allowed_vehicles = len(non_empty_trucks)
  trucks = trucks[:maximum_allowed_vehicles]

def initialize_distance_matrix():
  global distance_matrix
  distance_matrix = [[0]*len(customers) for x in range(len(customers))]
  for x in range(len(customers)):
    for y in range(x):
      distance = Customer.get_distance_between_customers(customers[x], customers[y])
      distance_matrix[x][y] = distance
      distance_matrix[y][x] = distance

def get_initial_solution():
  global distance_matrix, customers
  closest_allowed_neighbor = 0
  for truck in trucks:
    while truck.get_used_capacity() < vehicle_capacity and closest_allowed_neighbor != None:
      closest_allowed_neighbor = truck.get_closest_allowed_neighbor(distance_matrix, customers, vehicle_capacity)
      if closest_allowed_neighbor != None:
        truck.add_last_customer_visit( closest_allowed_neighbor )
    closest_allowed_neighbor = 0

def initialize_trucks():
  for x in range(maximum_allowed_vehicles):
    t = Truck(x + 1, [])
    trucks.append(t)

def show_plot():
  global depot
  n = len(customers)
  x = [element.x for element in customers[1:]]
  y = [element.y for element in customers[1:]]
  plt.scatter(x, y)
  plt.scatter(depot.x, depot.y, c="r")
  plt.show()

def initialize_customers_and_depot():
  global depot, maximum_allowed_vehicles, vehicle_capacity
  f = open(FILE_NAME, "r")
  lines = f.readlines()
  maximum_allowed_vehicles, vehicle_capacity = [int(element) for element in lines[4].split(" ") if element != '']
  for line in lines[9:]:
    args = [int(element) for element in line.split(" ") if element != '']
    customer = Customer(*args)
    customers.append(customer)
  depot = customers[0]
  depot.is_depot = True


main()