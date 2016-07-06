# brookarner22@gmail.com

import matplotlib.pyplot as plt
import ipdb
# ipdb.set_trace() <-- this is what lets you use the debugger

# first thing is we want to read the file of the solution

# solution_file_name = "../standard_instances/RC208_wr_solution.txt"
# instance_file_name = "../standard_instances/RC208.txt"

solution_file_name = "../standard_instances/C201_wr_solution.txt"
instance_file_name = "../standard_instances/C201.txt"

# to open a file, just name it and tell it what you want to do (so "r" = read, "w" = write)
solution_file = file( solution_file_name, "r" )

# takes each individual line in a file and turns it into a list, here called "lines_in_file"
lines_in_file = solution_file.readlines()

solution_file.close()

# saves 5th line of file into the variable on the LHS
truck_1 = lines_in_file[5]
# (a) removes the \n character; (b) interprets each piece of information split by a space; (c) starts at the 3rd index of the list
new_truck_1 = truck_1.strip().split(" ")[3:]
int_truck_1 = [ int(element) for element in new_truck_1 ]

# do it for the 6th line (second truck)
truck_2 = lines_in_file[6]
new_truck_2 = truck_2.strip().split(" ")[3:]
int_truck_2 = [ int(element) for element in new_truck_2 ]

# do it for the 7th line (third truck)
truck_3 = lines_in_file[7]
new_truck_3 = truck_3.strip().split(" ")[3:]
int_truck_3 = [ int(element) for element in new_truck_3 ]

# print it if you want to
# print int_truck_1
# print int_truck_2
# print int_truck_3

customers = []

instance_file = file( instance_file_name, "r" )

lines_in_file = instance_file.readlines()

instance_file.close()

# splits each line and inserts a new customer into the customers list with just [x, y] for each customer
for line in lines_in_file[5:]:
  split_line = line.rsplit()
  x = float(split_line[1])
  y = float(split_line[2])
  new_customer = [x, y]
  customers.append( new_customer )

# x and y for all customers
x = []
y = []

# going through all customers, call each one "customer" and then store the x and y coords of each
for customer in customers:
  x.append( customer[0] )
  y.append( customer[1] )

# plot the customers by referencing their x and y coordinates in the same order
plt.scatter(x, y)
plt.scatter(40.0, 50.0, c="r")

# truck 1
# set up the depot spot
x1 = [40.0]
y1 = [50.0]

# get the x and y coordinates of the customers that are visited by truck 1 in their proper order (!) from the solution file
for visit in int_truck_1:
  x1.append( customers[visit][0] )
  y1.append( customers[visit][1] )

# sending the truck back to the depot
x1.append( 40.0 )
y1.append( 50.0 )

# truck 1
x2 = [40.0]
y2 = [50.0]

for visit in int_truck_2:
  x2.append( customers[visit][0] )
  y2.append( customers[visit][1] )

x2.append( 40.0 )
y2.append( 50.0 )

# truck 1
x3 = [40.0]
y3 = [50.0]

for visit in int_truck_3:
  x3.append( customers[visit][0] )
  y3.append( customers[visit][1] )

x3.append( 40.0 )
y3.append( 50.0 )


# make a connected line plot for each truck by referencing their x and y coordinates sequentially
plt.plot( x1, y1, c = "r", linewidth = 2)
plt.plot( x2, y2, c = "b", linewidth = 2)
plt.plot( x3, y3, c = "k", linewidth = 2)

plt.show()