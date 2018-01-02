"""
Experiment: find a suitable modulus for a multi-stream Lehmer pseudo-random
generator.
"""

from core.rnd.inspection import modulus_finder
from core.utils.report import SimpleReport
from experiments import EXP_DIR, RES_EXT


_BITS = 8


def experiment(bits=_BITS):
    """
    Find a modulus for the given number of bits.
    :param bits: (int) number of bits; muyst be positive.
    """
    modulus = modulus_finder.find_modulus(bits)

    # Report
    r = SimpleReport('MODULUS')
    r.add('General', 'Bits', bits)
    r.add('Result', 'Modulus', modulus)
    r.save('%s/%s.%s' % (EXP_DIR, 'test-inspection-modulus', RES_EXT))

    print(r)


if __name__ == '__main__':
    experiment()