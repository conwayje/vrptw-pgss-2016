""" Class for plotting customer locations and paths.
"""
import matplotlib.pyplot as plt
from Customer import Customer
from Depot import Depot
from Path import Path

class Visual():

    subplot = plt.figure().add_subplot(111)

    @staticmethod
    def plot_customers(depot, customers, label = True, connect = False, color = 'b', marker = 'o', linewidth = 2.0):
        x = []
        y = []
        for customer in customers:
            x.append(customer.x)
            y.append(customer.y)
            if label:
                Visual.subplot.text(customer.x, customer.y, str(customer.number), weight='bold', size='smaller')
        plt.scatter(depot.x, depot.y, color = 'r')
        plt.scatter(x, y, color = color, marker = marker)
        if connect:
            plt.plot(x, y, color = color, linewidth = linewidth)

    @staticmethod
    def show():
        plt.show()

    @staticmethod
    def plot_path(path, color = 'b', marker = 'o', linewidth = 2.0):
      Visual.plot_customers(Depot(0,0), path.route, connect= True, color = color, marker = marker, linewidth= linewidth)