import threading
from math import sqrt
from rnd.inspection.multiplier import is_fp_multiplier, is_mc_multiplier


THREADS = 32
MULTIPLIER = 0


class MultiplierFinder(threading.Thread):

    def __init__(self, modulus, rng):
        threading.Thread.__init__(self)
        self.modulus = modulus
        self.rng = rng

    def run(self):
        global MULTIPLIER
        for multiplier in self.rng:
            print('Testing: %d' % multiplier)
            if MULTIPLIER != 0: break
            if is_mc_multiplier(multiplier, self.modulus) and is_fp_multiplier(multiplier, self.modulus):
                MULTIPLIER = multiplier
                break


def find_multiplier(modulus):
    mx = int(sqrt(modulus)) - 1
    pool = []
    for t in range(THREADS):
        #rng = range(mx - t, 0, -THREADS)
        rng = range(1+t, mx, THREADS)
        finder = MultiplierFinder(modulus, rng)
        pool.append(finder)
    for finder in pool:
        finder.start()
    for finder in pool:
        finder.join()
    return MULTIPLIER


def _test():
    """
    Tests the correctness of functions.
    """
    MODULUS = 2147483647  # 127 (8bit), 32749 (16bit), 2147483647 (32bit), 9223372036854775783 (64bit)
    fpmc_multiplier = find_multiplier(MODULUS)

    # Report
    print('======================================')
    print('INSPECTION: FP/MC MULTIPLIER          ')
    print('======================================')
    print('Modulus: %d' % MODULUS)
    print('--------------------------------------')
    print('Candidate: %d' % fpmc_multiplier)
    print('\n')


if __name__ == '__main__':
    _test()