"""
Experiment: find a suitable jumper for a multi-stream Lehmer pseudo-random
generator.
"""

from demule.rnd.inspection import jumper_finder


def _experiment():
    MODULUS = 127
    MULTIPLIER = 3
    STREAMS = 64

    jumper, jumpsize = jumper_finder.find_jumper(MODULUS, MULTIPLIER, STREAMS)

    # Report
    print('======================================')
    print('INSPECTION: JUMPER                    ')
    print('======================================')
    print('Modulus: %d' % MODULUS)
    print('Multiplier: %d' % MULTIPLIER)
    print('Streams: %d' % STREAMS)
    print('--------------------------------------')
    print('Candidate: %d' % jumper)
    print('Jump Size: %d' % jumpsize)
    print('\n')


if __name__ == '__main__':
    _experiment()