"""
Implementation of the Lehmer pseudo-random generator.

Keep in mind the following table:

╔════════════╦════════════════════════════════════════════════╗
║            ║                      BITS                      ║
║            ╠═════╦═══════╦════════════╦═════════════════════╣
║            ║ 8   ║ 16    ║ 32         ║ 64                  ║
╠════════════╬═════╬═══════╬════════════╬═════════════════════╣
║ MODULUS    ║ 127 ║ 32719 ║ 2147483647 ║ 9223372036854775783 ║
╠════════════╬═════╬═══════╬════════════╬═════════════════════╣
║ MULTIPLIER ║ 14  ║ 16374 ║ 48271      ║                     ║
╠════════════╬═════╬═══════╬════════════╬═════════════════════╣
║ STREAMS    ║ 64  ║ 128   ║ 256        ║ 512                 ║
╠════════════╬═════╬═══════╬════════════╬═════════════════════╣
║ JUMPER     ║     ║       ║ 22925      ║                     ║
╠════════════╬═════╬═══════╬════════════╬═════════════════════╣
║ CHECKV     ║     ║       ║ 399268537  ║                     ║
╠════════════╬═════╬═══════╬════════════╬═════════════════════╣
║ CHECKI     ║     ║       ║ 10000      ║                     ║
╚════════════╩═════╩═══════╩════════════╩═════════════════════╝
"""

from time import time


MODULUS = 2147483647
MULTIPLIER = 48271
ISEED = 1
STREAMS = 256
JUMPER = 22925

CHECK_VALUE = 399268537
CHECK_ITERS = 10000

seed = [int(ISEED)] * STREAMS
stream = 0
init = False


class MarcianiMultiStream(object):
    """
    Utility class to encapsulate rndgen functionalities.
    """

    def __init__(self, seed):
        self._seed = seed
        select_stream(0)
        plant_seeds(self._seed)

    def stream(self, stream):
        """
        Selects the current stream.
        :param stream: stream index in [0,STREAMS-1]
        :return:
        """
        select_stream(stream)

    def rnd(self):
        """
        Generates a pseudo-random number from uniform distribution in [0,1)
        :return: a uniform pseudo-random float in [0,1)
        """
        u = rnd()
        return u

    def rndn(self, n):
        """
        Generates n pseudo-random numbers from uniform distribution in [0,1)
        :return: a list of uniform pseudo-random floats in [0,1)
        """
        sample = []
        for i in range(0, n):
            u = rnd()
            sample.append(u)
        return sample


def rnd():
    """
    Generates a pseudo-random number from uniform distribution in [0,1).
    :return: (float) a uniform pseudo-random number in [0,1).
    """
    global seed

    Q = int(MODULUS / MULTIPLIER)
    R = int(MODULUS % MULTIPLIER)

    t = int(MULTIPLIER * (seed[stream] % Q) - R * int(seed[stream] / Q))
    if t > 0:
        seed[stream] = int(t)
    else:
        seed[stream] = int(t + MODULUS)

    return float(seed[stream] / MODULUS)


def select_stream(sid):
    """
    Selects the current stream.
    :param sid: stream index in [0,STREAMS-1].
    """
    global stream
    stream = sid % STREAMS
    if not init and stream != 0:
        plant_seeds(ISEED)


def plant_seeds(x):
    """
    Initializes all the streams of the generator.
    :param x: (int) the initial seed.
    """

    global init
    global stream
    global seed

    Q = int(MODULUS / JUMPER)
    R = int(MODULUS % JUMPER)

    init = True
    s = stream
    select_stream(0)
    put_seed(x)
    stream = s
    for j in range(1, STREAMS):
        x = int(JUMPER * (seed[j - 1] % Q) - R * int((seed[j - 1] / Q)))
    if x > 0:
        seed[j] = x
    else:
        seed[j] = x + MODULUS


def put_seed(x):
    """
    Initializes the current stream with the specified seed.
    :param x: (int) the seed.
    """
    global seed
    if x > 0:
        x = x % MODULUS
    else:
        x = time()
        x = x % MODULUS
    seed[stream] = int(x)


def get_seed():
    """
    Retrieves the seed of the current stream.
    :return: (int) the seed of the current stream.
    """
    return seed[stream]


def _test():
    """
    Tests the correctness of the pseudo-random generator.
    """
    ok = False

    select_stream(0)
    put_seed(1)
    for i in range(0, CHECK_ITERS):
        u = rnd()
    x = get_seed()
    ok = (x == CHECK_VALUE)

    select_stream(1)
    plant_seeds(1)
    x = get_seed()
    ok = (ok == True) and (x == JUMPER)
    if (ok == True):
        print("\nThe implementation of rndgen is correct")
    else:
        print("\nThe implementation of rndgen is not correct")


if __name__ == '__main__':
    _test()