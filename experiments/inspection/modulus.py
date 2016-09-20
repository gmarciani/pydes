"""
Experiment: find a suitable modulus for a multi-stream Lehmer pseudo-random
generator.
"""

from demule.rnd.inspection import modulus_finder
from experiments import EXP_DIR, RES_EXT


def experiment():
    BITS = 8

    modulus = modulus_finder.find_modulus(BITS)

    # Report
    report = \
        '======================================' + '\n' + \
        'INSPECTION: MODULUS                   ' + '\n' + \
        '======================================' + '\n' + \
        'Bits: %d' % (BITS,) + '\n' +\
        '--------------------------------------' + '\n' + \
        'Candidate: %d' % modulus + '\n\n'

    print(report)

    # Report on file
    filename = '%s/%s.%s' % (EXP_DIR, 'test-inspection-modulus', RES_EXT)
    with open(filename, 'w') as resfile:
        resfile.write(report)


if __name__ == '__main__':
    experiment()