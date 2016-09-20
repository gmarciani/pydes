"""
Implementation of the Lehmer pseudo-random generator.

Keep in mind the following table:

╔════════════╦════════════════════════════════════════════════╗
║            ║                      BITS                      ║
║            ╠═════╦═══════╦════════════╦═════════════════════╣
║            ║ 8   ║ 16    ║ 32         ║ 64                  ║
╠════════════╬═════╬═══════╬════════════╬═════════════════════╣
║ MODULUS    ║ 127 ║ 32479 ║ 2147483647 ║ 9223372036854775783 ║
╠════════════╬═════╬═══════╬════════════╬═════════════════════╣
║ MULTIPLIER ║ 14  ║ 16374 ║ 48271      ║                     ║
╠════════════╬═════╬═══════╬════════════╬═════════════════════╣
║ STREAMS    ║ 64  ║ 128   ║ 256        ║ 512                 ║
╠════════════╬═════╬═══════╬════════════╬═════════════════════╣
║ JUMPER     ║ 14  ║ 32748 ║ 22925      ║                     ║
╠════════════╬═════╬═══════╬════════════╬═════════════════════╣
║ CHECKV     ║     ║       ║ 399268537  ║                     ║
╠════════════╬═════╬═══════╬════════════╬═════════════════════╣
║ CHECKI     ║     ║       ║ 10000      ║                     ║
╚════════════╩═════╩═══════╩════════════╩═════════════════════╝
"""

_MODULUS = 2147483647
_MULTIPLIER = 48271
_ISEED = 1
_STREAMS = 256
_JUMPER = 22925

seed = [int(_ISEED)] * _STREAMS
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

    Q = int(_MODULUS / _MULTIPLIER)
    R = int(_MODULUS % _MULTIPLIER)

    t = int(_MULTIPLIER * (seed[stream] % Q) - R * int(seed[stream] / Q))
    if t > 0:
        seed[stream] = int(t)
    else:
        seed[stream] = int(t + _MODULUS)

    return float(seed[stream] / _MODULUS)


def select_stream(sid):
    """
    Selects the current stream.
    :param sid: stream index in [0,STREAMS-1].
    """
    global stream
    stream = sid % _STREAMS
    if init is False and stream != 0:
        plant_seeds(_ISEED)


def plant_seeds(x):
    """
    Initializes all the streams of the generator.
    :param x: (int) the initial seed.
    """

    global init
    global stream
    global seed

    Q = int(_MODULUS / _JUMPER)
    R = int(_MODULUS % _JUMPER)

    init = True
    s = stream
    select_stream(0)
    put_seed(x)
    stream = s
    for j in range(1, _STREAMS):
        x = int(_JUMPER * (seed[j - 1] % Q) - R * int((seed[j - 1] / Q)))
        if x > 0:
            seed[j] = x
        else:
            seed[j] = x + _MODULUS


def put_seed(x):
    """
    Initializes the current stream with the specified seed.
    :param x: (int) the seed.
    """
    global seed
    if x > 0:
        x %= _MODULUS
    seed[stream] = int(x)


def get_seed():
    """
    Retrieves the seed of the current stream.
    :return: (int) the seed of the current stream.
    """
    return seed[stream]