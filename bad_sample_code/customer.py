class Customer():
  def __init__(self, id_number, x, y, amount, open_time, close_time, service_duration):
    self.id_number = id_number
    self.x = x
    self.y = y
    self.amount = amount
    self.open_time = open_time
    self.close_time = close_time
    self.service_duration = service_duration
    self.is_serviced = False
    self.is_depot = False

  def __str__(self):
    return "<Customer #{}: ({}, {}) A: {}>".format(self.id_number, self.x, self.y, self.amount)

  def __unicode__(self):
    return "<Customer #{}: ({}, {}) A: {}>".format(self.id_number, self.x, self.y, self.amount)

  @staticmethod
  def get_distance_between_customers(customer_a, customer_b):
    x1, y1 = customer_a.x, customer_a.y
    x2, y2 = customer_b.x, customer_b.y
    return ( (x1 - x2)**2 + (y1 - y2)**2 )**0.5