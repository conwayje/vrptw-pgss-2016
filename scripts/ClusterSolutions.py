## Cluster Optimal Solution
## Hard coded cluster solutions
from Path import Path
from Customer import Customer
from Truck import Truck
from Cluster import Cluster

## ********************* CHECK SYNTAX *************************
class cluster_solutions():

	cluster_c_solutions = []
	cluster_rc_solutions = []

	def _init_ (self, customer, path, cluster_data, optimal_solution):
		self.customer = customer
		self.path = path
		self.cluster_data = cluster_data
		self.optimal_solution = optimal_solution

	# CLUSTERS FOR C201
	def c_cluster1(self):
		## Customers 39,36,34,38,37,33,32,35,31
		customer = [39,36,34,38,37,33,32,35,31]

		cluster_data = get_data(customer)
		optimal_solution = get_solution(customer) 

		cluster_c_solutions.append(optimal_solution)
		return cluster_c_solutions

	def c_cluster2(self):
		## Customers 16,14,12,19,15,18,17,13
		customer = [16,14,12,19,15,18,17,13]

		cluster_data = get_data(customer)
		optimal_solution = get_solution(customer)

		cluster_c_solutions.append(optimal_solution)
		return cluster_c_solutions

	def c_cluster3(self):
		## Customers 30,29,27,24,22,20,21
		customer = [30,29,27,24,22,20,21]

		cluster_data = get_data(customer)
		optimal_solution = get_solution(customer)
		
		cluster_c_solutions.append(optimal_solution)
		return cluster_c_solutions

	def c_cluster4(self):
		## Customers 52,47,43,50,42,41,51,45
		customer = [52,47,43,50,42,41,51,45]

		cluster_data = get_data(customer)
		optimal_solution = get_solution(customer)
		
		cluster_c_solutions.append(optimal_solution)
		return cluster_c_solutions

	def c_cluster5(self):
		## Customers 57,55,59,54,60,58,56,53
		customer = [57,55,59,54,60,58,56,53]

		cluster_data = get_data(customer)
		optimal_solution = get_solution(customer)
		
		cluster_c_solutions.append(optimal_solution)
		return cluster_c_solutions

	def c_cluster6(self):
		## Customers 67,63,69,66,62,74,64,61,72
		customer = [67,63,69,66,62,74,64,61,72]

		cluster_data = get_data(customer)
		optimal_solution = get_solution(customer)
		
		cluster_c_solutions.append(optimal_solution)
		return cluster_c_solutions

	def c_cluster7(self):
		## Customers 91,90,88,86,84,83,82
		customer = [91,90,88,86,84,83,82]

		cluster_data = get_data(customer)
		optimal_solution = get_solution(customer)
		
		cluster_c_solutions.append(optimal_solution)
		return cluster_c_solutions

	def c_cluster8(self):
		## Customers 81,76,71,79,73,70,80
		customer = [81,76,71,79,73,70,80]

		cluster_data = get_data(customer)
		optimal_solution = get_solution(customer)
		
		cluster_c_solutions.append(optimal_solution)
		return cluster_c_solutions

	# CLUSTERS FOR RC208

	def rc_cluster1(self):
		## Customers 17,47,14,12,16,15,11,10,13,9
		customer = [17,47,14,12,16,15,11,10,13,9]

		cluster_data = get_data(customer)
		optimal_solution = get_solution(customer)

		cluster_rc_solutions.append(optimal_solution)
		return cluster_rc_solutions

	def rc_cluster2(self):
		## Customers 5,3,1,45,8,46,4,7,6,2
		customer = [5,3,1,45,8,46,4,7,6,2]

		cluster_data = get_data(customer)
		optimal_solution = get_solution(customer)
		
		cluster_rc_solutions.append(optimal_solution)
		return cluster_rc_solutions


	def rc_cluster3(self):
 		## Customers 43,44,42,40,39,38,41,36,35,37
 		customer = [43,44,42,40,39,38,41,36,35,37]
		cluster_data = get_data(customer)
		optimal_solution = get_solution(customer)
		
		cluster_rc_solutions.append(optimal_solution)
		return cluster_rc_solutions


	def rc_cluster4(self):
		## Customers 34,31,29,27,32,30,28,26,33
		customer = [34,31,29,27,32,30,28,26,33]

		cluster_data = get_data(customer)
		optimal_solution = get_solution(customer)

		cluster_rc_solutions.append(optimal_solution)
		return cluster_rc_solutions


	def rc_cluster5(self):
		## Customers 24,22,20,49,19,25,23,21,48,18
		customer = [24,22,20,49,19,25,23,21,48,18]

		cluster_data = get_data(customer)
		optimal_solution = get_solution(customer)
		
		cluster_rc_solutions.append(optimal_solution)
		return cluster_rc_solutions













