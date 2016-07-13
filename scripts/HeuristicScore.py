# Heuristic Scoring
## Penalize for bad moves, reward for good moves (or for not being penalized)
from Path import Path
from Customer import Customer
from Truck import Truck

## STILL NEED PENALTIES FOR COMING OUT OF CLUSTERS AND OUTRAGEOUS ANGLE OF TURNING
class Heuristic_Score():

	def _init_(self, state, customer, truck):
		self.state = state
		self.customer = customer
		self.truck = truck

	def penalties(self):
		#placeholder paths until state is generated
		paths = state.get_paths
		customer = Customer(self.customer)
		truck = Truck(self.truck)
		# get the distance (benchmark score) from paths
		distance = paths.distance

		# get data
		did_cross = paths.intersect ## from 'Path.py'
		missed_customer = paths.missedCustomers ## from 'Path.py'
		capacity = truck.cargo ## from 'Truck.py'
		early_arrival = path.diff_time ## from 'Path.py'


		if (missed_customer == True):
			# ya done goofed
			distance += 10000000000000000000000000000000

		# #if (did_cross == True):
		# #	distance += 100

		# if (capacity == 0): 
		# 	# if the capacity of the truck reaches 0 at any time
		# 	distance += 500

		# if (diff_time > 0):
		# 	distance += early_arrival/2

		# for(customer in self.truck.path.route)
		# {

		# }



		


		
