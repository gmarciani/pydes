import threading
from demule.rnd.inspection.multiplier import is_mc_multiplier


_THREADS = 32
_JUMPER = 0
_JSIZE = 0


class JumperFinder(threading.Thread):

    def __init__(self, modulus, multiplier, rng):
        threading.Thread.__init__(self)
        self._modulus = modulus
        self._multiplier = multiplier
        self._rng = rng

    def run(self):
        global _JUMPER
        global _JSIZE
        for jsize in self._rng:
            if _JSIZE != 0: break
            jumper = (self._multiplier ** jsize) % self._modulus
            if is_mc_multiplier(jumper, self._modulus):
                _JUMPER = jumper
                _JSIZE = jsize
                break


def find_jumper(modulus, multiplier, streams, threads=_THREADS):
    mx = int(modulus + 1 / streams)
    pool = []
    for t in range(threads):
        rng = range(mx - t, 0, -threads)
        finder = JumperFinder(modulus, multiplier, rng)
        pool.append(finder)
    for finder in pool:
        finder.start()
    for finder in pool:
        finder.join()
    return _JUMPER, _JSIZE