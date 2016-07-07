""" Class for plotting customer locations and paths.
"""
import numpy as np
import matplotlib.pyplot as plt
from Customer import Customer
from Depot import Depot
from Path import Path

class Visual():

    @staticmethod
    def plot_customers(depot, customers, connect = False, color = 'b', marker = 'o', linewidth = 2.0):
        x = []
        y = []
        for customer in customers:
            x.append(customer.x)
            y.append(customer.y)
        plt.scatter(depot.x, depot.y, color = 'r')
        plt.scatter(x, y, color = color, marker = marker)
        if connect:
            plt.plot(x, y, color = color, linewidth = linewidth)
        plt.show()

    @staticmethod
    def plot_path(path, color = 'b', marker = 'o', linewidth = 2.0):
      Visual.plot_customers(path.route[0], path.route, connect= True, color = color, marker = marker, linewidth= linewidth)