import threading
from demule.common.mathutils import isprime


THREADS = 8
M = 0


class PrimeFinder(threading.Thread):

    def __init__(self, rng):
        threading.Thread.__init__(self)
        self.rng = rng

    def run(self):
        global M
        for m in self.rng:
            if M: break
            if isprime(m):
                M = m
                break


def find_modulus(bits):
    mx = 2**(bits - 1) - 1
    pool = []
    for t in range(THREADS):
        rng = range(mx, 0, -(t + 1))
        finder = PrimeFinder(rng)
        pool.append(finder)
    for finder in pool:
        finder.start()
    for finder in pool:
        finder.join()
    return M