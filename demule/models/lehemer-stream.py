from libs.des.rngs import random, putSeed, plantSeeds, selectStream


class LehemerStream:

    def __init__(self, seed):
        self._seed = seed
        selectStream(0)
        putSeed(self._seed)

    def rnd(self, s=0):
        selectStream(s)
        plantSeeds(self._seed)
        u = random()
        return u

    def rndn(self, n, s=0):
        sample = []
        selectStream(s)
        plantSeeds(self._seed)
        for i in range(0, n):
            u = random()
            sample.append(u)
        return sample

def _testLehemer():
    generator = LehemerStream(1)
    sample = generator.rndn(10, 0)
    print(sample)
    sample = generator.rndn(10, 1)
    print(sample)

if __name__ == '__main__':
    _testLehemer()