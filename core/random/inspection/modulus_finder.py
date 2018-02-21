import threading
from core.utils import mathutils


_THREADS = 32


class SharedModulus:

    lock = threading.Lock()

    def __init__(self):
        self.value = 0


class ModulusFinder(threading.Thread):

    def __init__(self, rng, modulus):
        threading.Thread.__init__(self)
        self.rng = rng
        self.modulus = modulus

    def run(self):
        for candidate in self.rng:
            if candidate < self.modulus.value:
                break
            if mathutils.is_prime(candidate):
                with self.modulus.lock:
                    if candidate > self.modulus.value:
                        self.modulus.value = candidate
                        break


def find_modulus(bits, threads=_THREADS):
    mx = 2**(bits - 1) - 1
    pool = []
    modulus = SharedModulus()
    for t in range(threads):
        rng = range(mx - t, 0, -threads)
        finder = ModulusFinder(rng, modulus)
        pool.append(finder)
    for finder in pool:
        finder.start()
    for finder in pool:
        finder.join()
    return modulus.value