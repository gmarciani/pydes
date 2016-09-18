import threading
from demule.rnd.inspection.multiplier import is_mc_multiplier

THREADS = 8
JUMPER = 0
JSIZE = 0


class JumperFinder(threading.Thread):

    def __init__(self, modulus, multiplier, rng):
        threading.Thread.__init__(self)
        self.modulus = modulus
        self.multiplier = multiplier
        self.rng = rng

    def run(self):
        global JUMPER
        global JSIZE
        for jsize in self.rng:
            if JSIZE != 0: break
            jumper = (self.multiplier ** jsize) % self.modulus
            if is_mc_multiplier(jumper, self.modulus):
                JUMPER = jumper
                JSIZE = jsize
                break


def find_jumper(modulus, multiplier, streams):
    mx = int(modulus + 1 / streams)
    pool = []
    for t in range(THREADS):
        rng = range(mx - t, 0, -THREADS)
        finder = JumperFinder(modulus, multiplier, rng)
        pool.append(finder)
    for finder in pool:
        finder.start()
    for finder in pool:
        finder.join()
    return JUMPER, JSIZE


if __name__ == '__main__':
    MODULUS = 2147483647    # 127 (8bit), 32749 (16bit), 2147483647 (32bit), 9223372036854775783 (64bit)
    MULTIPLIER = 48271      # -, -, 48271, -
    STREAMS = 256           # 256, 512, 1024, 2048

    jumper, jsize = find_jumper(MODULUS, MULTIPLIER, STREAMS)

    # Report
    print('======================================')
    print('INSPECTION: JUMPER                    ')
    print('======================================')
    print('Modulus: %d' % MODULUS)
    print('Multiplier: %d' % MULTIPLIER)
    print('Streams: %d' % STREAMS)
    print('--------------------------------------')
    print('Candidate: %d' % jumper)
    print('Jump Size: %d' % jsize)
    print('\n')

