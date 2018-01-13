import threading
from core.utils import mathutils


_MODULUS = 0


class ModulusFinder(threading.Thread):

    def __init__(self, rng):
        threading.Thread.__init__(self)
        self.rng = rng

    def run(self):
        global _MODULUS
        for modulus in self.rng:
            if _MODULUS != 0:
                break
            if mathutils.is_prime(modulus):
                _MODULUS = modulus
                break


def find_modulus(bits):
    threads = bits
    mx = 2**(bits - 1) - 1
    pool = []
    for t in range(threads):
        rng = range(mx - t, 0, -threads)
        finder = ModulusFinder(rng)
        pool.append(finder)
    for finder in pool:
        finder.start()
    for finder in pool:
        finder.join()
    return _MODULUS