import matplotlib.pyplot as plt
import ipdb

solution_file = "../standard_instances/RC208_wr_solution.txt"

f = file(solution_file, "r")
solution_lines = f.readlines()
f.close()

truck_1_path = solution_lines[5].strip()
truck_2_path = solution_lines[6].strip()
truck_3_path = solution_lines[7].strip()

truck_1_customers = truck_1_path.split(" ")[4:]
truck_2_customers = truck_2_path.split(" ")[4:]
truck_3_customers = truck_3_path.split(" ")[4:]

truck_1_customers = [float(element) for element in truck_1_customers]
truck_2_customers = [float(element) for element in truck_2_customers]
truck_3_customers = [float(element) for element in truck_3_customers]

customers = []
customer = [40, 50] # this is the depot

customers.append( customer )

instance_file = "../standard_instances/RC208.txt"

f = open( instance_file, "r" )
lines = f.readlines()
f.close()

for line in lines[6:]:
  parsed = line.rsplit()
  customers.append( [ float(parsed[1]), float(parsed[2]) ] )

truck_1 = [65, 83, 64, 95, 92, 71, 72, 38, 39, 44, 42, 61, 81, 94, 67, 62, 50, 34, 31, 29, 27, 26, 28, 30, 32, 33, 76, 89, 63, 85, 51, 84, 56, 66]
truck_2 = [69, 98, 88, 53, 12, 11, 15, 16, 47, 78, 73, 79, 7, 6, 2, 8, 46, 4, 45, 5, 3, 1, 43, 40, 36, 35, 37, 41, 54, 96, 93, 91, 80]
truck_3 = [90, 82, 99, 52, 57, 23, 21, 18, 19, 49, 22, 24, 20, 48, 25, 77, 58, 75, 97, 59, 87, 74, 86, 9, 13, 10, 14, 17, 60, 55, 100, 70, 68]

x = [element[0] for element in customers[1:]]
y = [element[1] for element in customers[1:]]
plt.scatter(x, y)
plt.scatter( customers[0][0], customers[0][1], c = 'r' )

x2 = [40.0]
y2 = [50.0]

x3 = [40.0]
y3 = [50.0]

x4 = [40.0]
y4 = [50.0]

for customer_id in truck_1:
  customer = customers[customer_id]
  x2.append( customer[0] )
  y2.append( customer[1] )

x2.append( 40.0 )
y2.append( 50.0 )

for customer_id in truck_2:
  customer = customers[customer_id]
  x3.append( customer[0] )
  y3.append( customer[1] )

x3.append( 40.0 )
y3.append( 50.0 )

for customer_id in truck_3:
  customer = customers[customer_id]
  x4.append( customer[0] )
  y4.append( customer[1] )

x4.append( 40.0 )
y4.append( 50.0 )

plt.plot(x2, y2, c = "b", linewidth = 2)
plt.plot(x3, y3, c = "g", linewidth = 2)
plt.plot(x4, y4, c = "k", linewidth = 2)


plt.show()