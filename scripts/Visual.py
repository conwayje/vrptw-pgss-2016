""" Class for plotting customer locations and paths.
"""
# import matplotlib.pyplot as plt
from Tkinter import *
from Customer import Customer
from Depot import Depot
from Path import Path

class Visual():

    width = 700
    height = 700
    root = Tk()
    canvas = Canvas(root, width=width, height=height)
    canvas.pack()
    root.title("Plot")

    @staticmethod
    def scale_x(x):
        return x * 5 + Visual.width/2
    @staticmethod
    def scale_y(y):
        return -y * 5 + Visual.height/2
    @staticmethod
    def scale(item):
        return Visual.scale_x(item.x), Visual.scale_y(item.y)

    @staticmethod
    def plot_customers(depot, customers, label = True, connect = False, color = 'blue', width = 2):

        list = [depot]
        for customer in customers:
            list.append(customer)
        list.append(depot)

        Visual.canvas.create_rectangle(Visual.scale(depot), Visual.scale(depot)[0] + 5, Visual.scale(depot)[1] + 5, fill = 'red')
        if connect:
            for i in range(len(list) - 1):
                Visual.canvas.create_line(Visual.scale(list[i]), Visual.scale(list[i+1]), fill = color, width = 2)
        if label:
            for c in customers:
                Visual.canvas.create_text(Visual.scale(c), text=str(c.number))

        Visual.root.update()

    @staticmethod
    def clear():
        Visual.canvas.delete(ALL)

    @staticmethod
    def plot_path(path, connect='True', color = 'blue', width = 2):
        Visual.plot_customers(Depot(0,0), path.route, connect = connect, color = color, width = width)

    @staticmethod
    def plot_customers_old(depot, customers, label = True, connect = False, color = 'b', marker = 'o', linewidth = 2.0):
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
            x.insert(0, depot.x)
            y.insert(0, depot.y)
            x.append(depot.x)
            y.append(depot.y)
            plt.plot(x, y, color = color, linewidth = linewidth)

    @staticmethod
    def plot_path_old(path, connect='True', color = 'b', marker = 'o', linewidth = 2.0):
        Visual.plot_customers(Depot(0,0), path.route, connect = connect, color = color, marker = marker, linewidth= linewidth)\

    @staticmethod
    def show():
        plt.show()