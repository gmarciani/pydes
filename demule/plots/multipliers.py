"""
Collection of functions to build Matplotlib plots for the multiplier analysis.
"""

import os
import matplotlib.pyplot as plt
import numpy as np
from demule.plots import *


def scatter(data, modulus, title=None, filename=None):
    y_fp = 3
    y_mc = 2
    y_fpmc = 1

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    ax.scatter(data[0], [y_fp]*len(data[0]), color=BLACK, marker='|')
    ax.scatter(data[1], [y_mc]*len(data[1]), color=BLACK, marker='|')
    ax.scatter(data[2], [y_fpmc]*len(data[2]), color=BLACK, marker='|')

    ax.axhline(y=y_fp, linestyle='solid', linewidth=0.3)
    ax.axhline(y=y_mc, linestyle='solid', linewidth=0.3)
    ax.axhline(y=y_fpmc, linestyle='solid', linewidth=0.3)

    if title is not None:
        ax.set_title(title)
    #ax.set_xlabel('$Values$')
    #ax.set_ylabel('$Multipliers$')

    ax.set_xlim(0, modulus-1)

    ax.set_xticks(np.linspace(0, modulus -1, 6))
    ax.set_yticks([y_fpmc, y_mc, y_fp])
    ax.set_yticklabels(['$FP/MC$', '$MC$','$FP$'])

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    ax.tick_params(axis='x', direction='out')
    ax.tick_params(axis='y', direction='out', length=0)
    for spine in ax.spines.values():
        spine.set_position(('outward', 5))
    ax.set_axisbelow(True)

    if filename is not None:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        plt.savefig(filename, bbox_inches='tight')
    else:
        fig.show()

    plt.close(fig)
