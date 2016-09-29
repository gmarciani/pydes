"""
Experiment: find a suitable modulus for a multi-stream Lehmer pseudo-random
generator.
"""

from demule.rnd.inspection import modulus_finder
from demule.utils.report import SimpleReport
from experiments import EXP_DIR, RES_EXT


def experiment():
    BITS = 8

    modulus = modulus_finder.find_modulus(BITS)

    # Report
    r = SimpleReport('MODULUS')
    r.add('General', 'Bits', BITS)
    r.add('Result', 'Modulus', modulus)
    r.save('%s/%s.%s' % (EXP_DIR, 'test-inspection-modulus', RES_EXT))

    print(r)


if __name__ == '__main__':
    experiment()