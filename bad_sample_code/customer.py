class Customer():
  # this is called auotmatically whenever you make a new instance of this class type.
  # in this case, i'm passing in a bunch of information and then setting instance variables
  # to contain that information.
  # to call this, you just have to do:
  #### CODE
  # new_customer = Customer( 1, 0.0, 0.0, 50.0, 12.0, 150.0, 90.0 )
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

  # these two methods work on any single instance of a Customer, so they're called something like:
  #### CODE:
  # customer = somehow_get_an_arbitrary_customer()
  # customer.do_something()

  # python has some special function that have names like __thisstyle__
  # these ones happen to be called like this:
  #### CODE:
  # customer = somehow_get_an_arbitrary_customer()
  # print customer
  def __str__(self):
    return "<Customer #{}: ({}, {}) A: {}>".format(self.id_number, self.x, self.y, self.amount)

  def __unicode__(self):
    return "<Customer #{}: ({}, {}) A: {}>".format(self.id_number, self.x, self.y, self.amount)


  # this method only works on the class called Customer itself, so it's called like:
  #### CODE
  # distance = Customer.get_distance_between_customers( customer_a, customer_b )
  @staticmethod
  def get_distance_between_customers(customer_a, customer_b):
    x1, y1 = customer_a.x, customer_a.y
    x2, y2 = customer_b.x, customer_b.y
    return ( (x1 - x2)**2 + (y1 - y2)**2 )**0.5