class Truck():
    #class for Truck
    def __init__(self, number, x, y, cargo, visited, distance):
        self.number = number #truck id/number
        self.x = x #x location
        self.y = y #y location
        self.cargo = cargo #amount of cargo currently in truck
        self.visited = visited #array of customers previously visited
        self.distance = distance #total distance traveled
        
    def __str__(self):
        return "<Truck {0}: x = {1}, y = {2}, cargo = {3}, visited = {4}, distance = {5}>".format(self.number, self.x, self.y, self.cargo, self.visited, self.distance)
        
    def distance_to_customer(self, cust): #distance to a given customer
        return ((cust.y - self.y)**2 + (cust.x - self.x)**2)**0.5
        
    def distance_from_depot(self): #distance from depot
        return (self.y**2 + self.x**2)**0.5
    
    