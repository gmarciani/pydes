from plots import *
import matplotlib.pyplot as plt


def scatter2D(title, data, filename=None):

    x = [result[0] for result in data]
    y = [result[1] for result in data]

    plt.scatter(x, y, color=BLUE)

    plt.suptitle(title)
    plt.xlabel('First')
    plt.ylabel('Second')
    plt.xlim(0, 1)
    plt.ylim(0, 1)

    if filename is None:
        plt.show()
    else:
        plt.savefig(filename)