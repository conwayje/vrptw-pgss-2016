import matplotlib.pyplot as plt
import ipdb

solution_file = "../standard_instances/C201_wr_solution.txt"

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

instance_file = "../standard_instances/C201.txt"

f = open( instance_file, "r" )
lines = f.readlines()
f.close()

for line in lines[6:]:
  parsed = line.rsplit()
  customers.append( [ float(parsed[1]), float(parsed[2]) ] )

truck_1 = [93, 5, 75, 2, 1, 99, 100, 97, 92, 94, 95, 98, 7, 3, 4, 89, 91, 88, 84, 86, 83, 82, 85, 76, 71, 70, 73, 80, 79, 81, 78, 77, 96, 87, 90]
truck_2 = [67, 63, 62, 74, 72, 61, 64, 66, 69, 68, 65, 49, 55, 54, 53, 56, 58, 60, 59, 57, 40, 44, 46, 45, 51, 50, 52, 47, 43, 42, 41, 48]
truck_3 = [20, 22, 24, 27, 30, 29, 6, 32, 33, 31, 35, 37, 38, 39, 36, 34, 28, 26, 23, 18, 19, 16, 14, 12, 15, 17, 13, 25, 9, 11, 10, 8, 21]

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