import matplotlib.pyplot as plt
import numpy as np
from plots import *

def scatter2D(data, title=None, filename=None, zoom=None):

    x = [result[0] for result in data]
    y = [result[1] for result in data]

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    ax.scatter(x, y, color=BLACK)

    if title is not None:
        ax.set_title(title)
    ax.set_xlabel('$1^{st}$')
    ax.set_ylabel('$2^{nd}$')

    if zoom is not None:
        s = zoom[0]
        e = zoom[1]
        ax.set_xlim(s, e)
        ax.set_ylim(s, e)
        ax.set_xticks(np.linspace(s, e, 6))
        ax.set_yticks(np.linspace(s, e, 6))
    else:
        ax.set_xticks(np.linspace(0, 1, 6))
        ax.set_yticks(np.linspace(0, 1, 6))

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(True)
    ax.set_axisbelow(True)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    ax.tick_params(axis='x', direction='out')
    #ax.tick_params(axis='y', length=0)
    ax.tick_params(axis='y', direction='out')
    if zoom is not None:
        for spine in ax.spines.values():
            spine.set_position(('data', zoom[0]))
        else:
            for spine in ax.spines.values():
                spine.set_position(('outward', 5))

    if filename is not None:
        plt.savefig(filename, bbox_inches='tight')
    else:
        fig.show()