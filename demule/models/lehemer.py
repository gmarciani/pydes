from libs.des.rng import random, putSeed


class Lehemer:

    def __init__(self, seed):
        self._seed = seed
        putSeed(self._seed)

    def rndn(self, n):
        sample = []
        for i in range(0, n):
            u = random()
            sample.append(u)
        return sample

def _testLehemer():
    generator = Lehemer(1)
    sample = generator.rndn(10)
    print(sample)

if __name__ == '__main__':
    _testLehemer()


