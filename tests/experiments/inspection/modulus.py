"""
Experiment: find a suitable modulus for a multi-stream Lehmer pseudo-random
generator.
"""

from demule.rnd.inspection import modulus_finder


def _experiment():
    BITS = 8

    modulus = modulus_finder.find_modulus(BITS)

    # Report
    print('======================================')
    print('INSPECTION: MODULUS                   ')
    print('======================================')
    print('Bits: %d' % BITS)
    print('--------------------------------------')
    print('Candidate: %d' % modulus)
    print('\n')

if __name__ == '__main__':
    _experiment()