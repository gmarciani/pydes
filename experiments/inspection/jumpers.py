"""
Experiment: find a suitable jumper for a multi-stream Lehmer pseudo-random
generator.
"""

from demule.rnd.inspection import jumper_finder
from demule.utils.report import SimpleReport
from experiments import EXP_DIR,RES_EXT


def experiment():
    MODULUS = 127
    MULTIPLIER = 3
    STREAMS = 64

    jumper, jumpsize = jumper_finder.find_jumper(MODULUS, MULTIPLIER, STREAMS)

    # Report
    r = SimpleReport('JUMPER')
    r.add('General', 'Modulus', MODULUS)
    r.add('General', 'Multiplier', MULTIPLIER)
    r.add('General', 'Streams', STREAMS)
    r.add('Result', 'Jumper', jumper)
    r.add('Result', 'Jump Size', jumpsize)
    r.save('%s/%s.%s' % (EXP_DIR, 'test-inspection-jumper', RES_EXT))

    print(r)


if __name__ == '__main__':
    experiment()