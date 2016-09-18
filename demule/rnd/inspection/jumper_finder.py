import threading
from demule.rnd.inspection.multiplier import is_mc_multiplier

THREADS = 8
JUMPER = 0

class JumperFinder(threading.Thread):

    def __init__(self, modulus, rng):
        threading.Thread.__init__(self)
        self.modulus = modulus
        self.rng = rng

    def run(self):
        global JUMPER
        for jumper in self.rng:
            if JUMPER != 0: break
            if is_mc_multiplier(jumper, self.modulus):
                JUMPER = jumper
                break


def find_jumper(modulus, streams):
    mx = int(modulus + 1 / streams)
    pool = []
    for t in range(THREADS):
        rng = range(mx - t, 0, -THREADS)
        finder = JumperFinder(modulus, rng)
        pool.append(finder)
    for finder in pool:
        finder.start()
    for finder in pool:
        finder.join()
    return JUMPER


if __name__ == '__main__':
    MODULUS = 127  # 127 (8bit), 32749 (16bit), 2147483647 (32bit), 9223372036854775783 (64bit)
    STREAMS = 256  # 256, 512, 1024, 2048

    jumper = find_jumper(MODULUS, STREAMS)

    # Report
    print('======================================')
    print('INSPECTION: JUMPER                    ')
    print('======================================')
    print('Modulus: %d' % MODULUS)
    print('Streams: %d' % MODULUS)
    print('--------------------------------------')
    print('Candidate: %d' % jumper)
    print('\n')

