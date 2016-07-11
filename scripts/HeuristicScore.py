# Heuristic Scoring
## Penalize for bad moves, reward for good moves (or for not being penalized)
from Path import Path
from Customer import Customer
from Truck import Truck

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
		missed_customer = paths.missedCustomer ## from 'Path.py'
		
		


		
