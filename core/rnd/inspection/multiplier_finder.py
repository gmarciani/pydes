import threading
from math import sqrt
from core.rnd.inspection.multiplier_check import is_fp_multiplier, is_mc_multiplier


_THREADS = 32


class SharedMultiplier:

    lock = threading.Lock()

    def __init__(self):
        self.value = 0


class MultiplierFinder(threading.Thread):

    def __init__(self, modulus, rng, multiplier):
        threading.Thread.__init__(self)
        self.modulus = modulus
        self.rng = rng
        self.multiplier = multiplier

    def run(self):
        for candidate in self.rng:
            if self.multiplier.value != 0:
                break
            if is_mc_multiplier(candidate, self.modulus) and is_fp_multiplier(candidate, self.modulus):
                with self.multiplier.lock:
                    if candidate > self.multiplier.value:
                        self.multiplier.value = candidate
                        break


def find_multiplier(modulus, threads=_THREADS):
    mx = int(sqrt(modulus)) - 1
    pool = []
    multiplier = SharedMultiplier()
    for t in range(threads):
        rng = range(1 + t, mx, threads)
        finder = MultiplierFinder(modulus, rng, multiplier)
        pool.append(finder)
    for finder in pool:
        finder.start()
    for finder in pool:
        finder.join()
    return multiplier.value