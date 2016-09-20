"""
Collection of functions to build Matplotlib plots for Chi-Square Tests.
"""


import matplotlib.pyplot as plt
from demule.plots import *


def scatter(data, mn, mx, title=None, filename=None):
    streams = len(data)

    data_in = [v for v in data if mn <= v[1] <= mx]
    data_out = [v for v in data if v[1] < mn or v[1] > mx]

    x_in = [v[0] for v in data_in]
    y_in = [v[1] for v in data_in]
    x_out = [v[0] for v in data_out]
    y_out = [v[1] for v in data_out]

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    ax.scatter(x_in, y_in, color=BLACK)
    ax.scatter(x_out, y_out, color=LGRAY)
    ax.axhline(y=mn, linestyle='dashed')
    ax.axhline(y=mx, linestyle='dashed')

    if title is not None:
        ax.set_title(title)
    ax.set_xlabel('$Stream$')
    ax.set_ylabel('$\chi^{2}$', rotation=0)

    ax.set_xticks([0, streams - 1])
    ax.set_yticks([mn, mx])
    ax.set_yticklabels(['$\chi^{2}_{min}$', '$\chi^{2}_{max}$'])

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

    if filename is not None:
        plt.savefig(filename, bbox_inches='tight')
    else:
        fig.show()

    plt.close(fig)
