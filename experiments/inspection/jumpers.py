"""
Experiment: find a suitable jumper for a multi-stream Lehmer pseudo-random
generator.
"""

from demule.rnd.inspection import jumper_finder
from experiments import EXP_DIR,RES_EXT


def experiment():
    MODULUS = 127
    MULTIPLIER = 3
    STREAMS = 64

    jumper, jumpsize = jumper_finder.find_jumper(MODULUS, MULTIPLIER, STREAMS)

    # Report
    report = \
        '======================================' + '\n' + \
        'INSPECTION: JUMPER                    ' + '\n' + \
        '======================================' + '\n' + \
        'Modulus: %d' % (MODULUS,) + '\n' + \
        'Multiplier: %d' % (MULTIPLIER,) + '\n' + \
        'Streams: %d' % (STREAMS,) + '\n' + \
        '--------------------------------------' + '\n' + \
        'Candidate: %d' % jumper + '\n' + \
        'Jump Size: %d' % jumpsize + '\n\n'

    print(report)

    # Report on file
    filename = '%s/%s.%s' % (EXP_DIR, 'test-inspection-jumper', RES_EXT)
    with open(filename, 'w') as resfile:
        resfile.write(report)


if __name__ == '__main__':
    experiment()