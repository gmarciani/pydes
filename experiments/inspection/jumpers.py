"""
Experiment: find a suitable jumper for a multi-stream Lehmer pseudo-random
generator.
"""

from core.random.inspection import jumper_finder
from core.utils.report import SimpleReport
from experiments import EXP_DIR,RES_EXT


_MODULUS = 127
_MULTIPLIER = 3
_STREAMS = 64


def experiment(modulus=_MODULUS,
               multiplier=_MULTIPLIER,
               streams=_STREAMS):

    jumper, jumpsize = jumper_finder.find_jumper(modulus, multiplier, streams)

    # Report
    r = SimpleReport('JUMPER')
    r.add('General', 'Modulus', modulus)
    r.add('General', 'Multiplier', multiplier)
    r.add('General', 'Streams', streams)
    r.add('Result', 'Jumper', jumper)
    r.add('Result', 'Jump Size', jumpsize)
    r.save('%s/%s.%s' % (EXP_DIR, 'test-inspection-jumper', RES_EXT))

    print(r)


if __name__ == '__main__':
    experiment()