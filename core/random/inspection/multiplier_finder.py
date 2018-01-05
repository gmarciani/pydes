import threading
from math import sqrt
from core.random.inspection.multiplier import is_fp_multiplier, is_mc_multiplier


_THREADS = 32
_MULTIPLIER = 0


class MultiplierFinder(threading.Thread):

    def __init__(self, modulus, rng):
        threading.Thread.__init__(self)
        self._modulus = modulus
        self._rng = rng

    def run(self):
        global _MULTIPLIER
        for multiplier in self._rng:
            if _MULTIPLIER != 0: break
            if is_mc_multiplier(multiplier, self._modulus) and is_fp_multiplier(multiplier, self._modulus):
                _MULTIPLIER = multiplier
                break


def find_multiplier(modulus, threads=_THREADS):
    mx = int(sqrt(modulus)) - 1
    pool = []
    for t in range(threads):
        rng = range(1 + t, mx, threads)
        finder = MultiplierFinder(modulus, rng)
        pool.append(finder)
    for finder in pool:
        finder.start()
    for finder in pool:
        finder.join()
    return _MULTIPLIER