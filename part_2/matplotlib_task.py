import math
import numpy as np
import pylab
from matplotlib import pyplot as plt
from matplotlib.lines import Line2D


def many_graph(x_list):
    """
    :param x_list:
    """
    plt.title(many_graph.__name__, fontsize=16)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.xlim(15)
    plt.ylim(10)

    def g():
        y_list = []
        for x in x_list:
            y_list.append(math.sin(x))
        return y_list

    hyperbola = Line2D(
        x_list[1:],
        [1/x for x in x_list[1:]],
        linestyle='solid',
        color='red',
    )
    sinusoid = Line2D(
        x_list,
        [math.sin(x) for x in x_list],
        linestyle='dashed',
        color='blue',
    )

    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.add_line(hyperbola)
    ax.add_line(sinusoid)

    plt.show()


if __name__ == '__main__':
    steps = [i for i in range(0, 25)]
    many_graph(steps)
