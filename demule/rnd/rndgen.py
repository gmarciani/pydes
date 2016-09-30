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
_ISEED = 123456789
_STREAMS = 256
_JUMPER = 22925

seed = [int(_ISEED)] * _STREAMS
stream = 0
init = False


class MarcianiMultiStream(object):
    """
    Utility class to encapsulate rndgen functionalities.
    """

    def __init__(self, iseed=_ISEED,
                 modulus=_MODULUS,
                 multiplier=_MULTIPLIER,
                 streams=_STREAMS,
                 jumper=_JUMPER):
        """
        Creates a new random number generator.
        :param iseed: (int) the initial seed; must be positive.
        Default is 123456789.
        :param modulus: (int) the modulus; must be positive and prime.
        Default is 2147483647.
        :param multiplier: (int) the multiplier; must be a FP/MC multiplier of
        *modulus*.
        Default is 48271.
        :param streams: (int) the number of disjoint streams; must be positive.
        Default is 256.
        :param jumper: (int) the jumper for the given streams; must be a
        suitable jumper for the given number of *streams*.
        Default is 22925.
        """
        self._iseed = self._seed = iseed
        self._stream = 0
        self._modulus = modulus
        self._multiplier = multiplier
        self._streams = streams
        self._jumper = jumper

        self._init = False

        self._seeds = [int(self._iseed)] * self._streams
        self.plant_seeds(self._iseed)

    def plant_seeds(self, x):
        """
        Initializes all the streams of the generator.
        :param x: (int) the initial seed.
        """
        #self._seed = x
        #self.stream(0)
        #plant_seeds(self._seed)

        Q = int(self._modulus / self._jumper)
        R = int(self._modulus % self._jumper)

        self._init = True
        s = self._stream
        self.stream(0)
        self.put_seed(x)
        self._stream = s
        for j in range(1, self._streams):
            x = int(self._jumper * (self._seeds[j - 1] % Q) - R * int((self._seeds[j - 1] / Q)))
            if x > 0:
                self._seeds[j] = x
            else:
                self._seeds[j] = x + self._modulus

    def get_seed(self):
        """
        Retrieves the seed of the current stream.
        :return: (int) the seed of the current stream.
        """
        return self._seeds[self._stream]

    def put_seed(self, x):
        """
        Initializes the current stream with the specified seed.
        :param x: (int) the seed.
        """
        if x > 0:
            x %= self._modulus
        else:
            raise ValueError(
                'x must be a positive number in (0, modulus). Found {}'.format(
                    x))
        self._seeds[self._stream] = int(x)

    def stream(self, stream_id):
        """
        Selects the current stream.
        :param stream_id: stream index in [0,STREAMS-1]
        """
        self._stream = stream_id % self._streams
        if self._init is False and self._stream != 0:
            self.plant_seeds(self._iseed)

    def rnd(self):
        """
        Generates a pseudo-random number from uniform distribution in [0,1)
        :return: a uniform pseudo-random float in [0,1)
        """
        Q = int(self._modulus / self._multiplier)
        R = int(self._modulus % self._multiplier)

        t = int(self._multiplier * (self._seeds[self._stream] % Q) -
                R * int(self._seeds[self._stream] / Q))
        if t > 0:
            self._seeds[stream] = int(t)
        else:
            self._seeds[stream] = int(t + self._modulus)

        return float(self._seeds[self._stream] / self._modulus)

    def rndn(self, n):
        """
        Generates a list of pseudo-random numbers from uniform distribution in
        [0,1)
        :param n: (int) number of random numbers to generate
        :return: (list(float)) a list of uniform pseudo-random numbers.
        """
        sample = []
        for i in range(0, n):
            u = self.rnd()
            sample.append(u)
        return sample