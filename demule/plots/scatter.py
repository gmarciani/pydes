"""
Collection of functions to build Matplotlib scatterplots.
"""


import matplotlib.pyplot as plt
from demule.utils import mathutils
import numpy as np
from demule.plots import *


def bivariate_scatterplot(sample, title=None, filename=None):
    u = [value[0] for value in sample]
    v = [value[1] for value in sample]

    U = np.arange(min(u), max(u), 0.001)
    r = mathutils.correlation_coefficient(sample)
    lrline = mathutils.linear_regression_line(sample)

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    ax.scatter(u, v, color=BLACK)
    ax.plot(U, lrline(U), linestyle='dashed')

    if title is not None:
        ax.set_title(title)
    ax.set_xlabel('$u$')
    ax.set_ylabel('$v$', rotation=0)

    ax.set_xticks([min(u), max(u)])
    ax.set_yticks([min(v), max(v)])

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(True)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    ax.tick_params(axis='x', direction='out')
    ax.tick_params(axis='y', direction='out')
    for spine in ax.spines.values():
        spine.set_position(('outward', 5))
    ax.set_axisbelow(True)

    ax.text(0.9, 0.1, 'r:%.3f'%r, ha='center', va='center',
            transform=ax.transAxes,
            bbox=dict(boxstyle='square', fc='#ffffff', ec='#000000'))

    if filename is not None:
        plt.savefig(filename, bbox_inches='tight')
    else:
        fig.show()

    plt.close(fig)