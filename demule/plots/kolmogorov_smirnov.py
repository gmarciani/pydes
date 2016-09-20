"""
Collection of functions to build Matplotlib plots for the Kolmogorov-Smirnov
Test.
"""


import matplotlib.pyplot as plt
import numpy as np
from demule.utils.rvms import cdfChisquare
from plots import *


def histogram(ksdistances, kspoint, kscritical, title=None, filename=None):
    samsize = len(ksdistances)

    x_in = [v[0] for v in ksdistances if v[1] <= kscritical]
    y_in = [v[1] for v in ksdistances if v[1] <= kscritical]

    x_out = [v[0] for v in ksdistances if v[1] > kscritical]
    y_out = [v[1] for v in ksdistances if v[1] > kscritical]

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    ax.bar(x_in, y_in, color=BLACK)
    ax.bar(x_out, y_out, color=LGRAY)
    ax.axhline(y=kscritical, linestyle='dashed')

    if title is not None:
        ax.set_title(title)
    ax.set_xlabel('$\chi^{2}_{i}$')
    ax.set_ylabel('$KS_{distance}$')

    ax.set_xticks([0, ksdistances[-1][0]])
    ax.set_yticks([0, kscritical])
    ax.set_xticklabels(['$\chi^{2}_{0}$', '$\chi^{2}_{%s}$' % (samsize-1)])
    ax.set_yticklabels(['$0$', '$KS_{critical}$'])

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

    ax.annotate('$KS_{statistic}$', xy=kspoint, xycoords='data',
                xytext=(-50, 30), textcoords='offset points',
                arrowprops=dict(arrowstyle="->")
                )

    if filename is not None:
        plt.savefig(filename, bbox_inches='tight')
    else:
        plt.show()


def histogram2(chisquares, bins, kspoint, title=None, filename=None):
    chisquares.sort(key=lambda v: v[1])

    streams = len(chisquares)

    chis = np.array([v[1] for v in chisquares])

    func_thr = lambda x: cdfChisquare(bins - 1, x)

    func_emp = lambda x: sum(i <= x for i in chis) / streams

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    ax.plot(chis, [func_thr(chi) for chi in chis], color=LGRAY, label='Theoretical')
    ax.step(chis, [func_emp(chi) for chi in chis], color=BLACK, label='Empirical')

    ax.axvline(x=kspoint[0], linestyle='dashed')

    if title is not None:
        ax.set_title(title)
    #ax.set_xlabel('$\chi^{2}_{i}$')
    ax.set_ylabel('$cdf$')

    ax.set_xticks([chis[0], kspoint[0], chis[-1]])
    ax.set_xticklabels(['$\chi^{2}_{0}$', '$\overline{\chi}^{2}_{i}$', '$\chi^{2}_{%s}$' % (streams - 1)])

    ax.set_yticks([0, 1])

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

    ax.legend(loc='lower right')

    if filename is not None:
        plt.savefig(filename, bbox_inches='tight')
    else:
        plt.show()