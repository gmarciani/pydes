"""
Collection of functions to build Matplotlib boxplots.
"""

import os
import matplotlib.pyplot as plt
from demule.utils import mathutils
import numpy as np
from demule.plots import *


def batch_means(domain, means, intervals, replications, theoretical=None, title=None, filename=None):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    plt.errorbar(domain, means, intervals, fmt='o')

    if theoretical is not None:
        ax.axhline(y=theoretical, linestyle='dashed')

    if title is not None:
        ax.set_title(title)
    ax.set_xlabel('$time$')
    ax.set_ylabel('$value$', rotation=0)

    ax.set_xticks([min(data.keys()), max(data.keys())])
    #ax.set_yticks([min(v), max(v)])

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

    ax.text(0.9, 0.1, 'replications:%d'%replications, ha='center', va='center',
            transform=ax.transAxes,
            bbox=dict(boxstyle='square', fc='#ffffff', ec='#000000'))

    if filename is not None:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        plt.savefig(filename, bbox_inches='tight')
    else:
        fig.show()

    plt.close(fig)