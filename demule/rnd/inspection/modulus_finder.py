import threading
from demule.utils.mathutils import isprime


THREADS = 8
MODULUS = 0


class ModulusFinder(threading.Thread):

    def __init__(self, rng):
        threading.Thread.__init__(self)
        self.rng = rng

    def run(self):
        global MODULUS
        for modulus in self.rng:
            if MODULUS != 0: break
            if isprime(modulus):
                MODULUS = modulus
                break


def find_modulus(bits):
    mx = 2**(bits - 1) - 1
    pool = []
    for t in range(THREADS):
        rng = range(mx - t, 0, -THREADS)
        finder = ModulusFinder(rng)
        pool.append(finder)
    for finder in pool:
        finder.start()
    for finder in pool:
        finder.join()
    return MODULUS


if __name__ == '__main__':
    BITS = 32  # 8, 16, 32, 64

    modulus = find_modulus(BITS)

    # Report
    print('======================================')
    print('INSPECTION: MODULUS                   ')
    print('======================================')
    print('Bits: %d' % BITS)
    print('--------------------------------------')
    print('Candidate: %d' % modulus)
    print('\n')