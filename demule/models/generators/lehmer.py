from libs.des.rng import random, putSeed


class Lehmer:

    def __init__(self, seed):
        self._seed = seed
        putSeed(self._seed)

    def rnd(self):
        u = random()
        return u

    def rndn(self, n):
        sample = []
        for i in range(0, n):
            u = random()
            sample.append(u)
        return sample

def _testLehmer():
    generator = Lehmer(1)
    r = generator.rnd()
    print(r)
    sample = generator.rndn(10)
    print(sample)

if __name__ == '__main__':
    _testLehmer()


