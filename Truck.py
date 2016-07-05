class Truck():
    #class for Truck
    def __init__(self, x, y, cargo, visited, distance):
        self.x = x #x location
        self.y = y #y location
        self.cargo = cargo #amount of cargo currently in truck
        self.visited = visited #array of customers previously visited
        self.distance = distance #total distance traveled
        
    def intersects_path(self): #whether the truck intersects its own path
        
        return True
        
    def distance_to_customer(self, cust): #distance to a given customer
        return ((cust.y - self.y)**2 + (cust.x - self.x)**2)**0.5
        
        