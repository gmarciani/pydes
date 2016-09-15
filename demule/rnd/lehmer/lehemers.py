from libs.des.rngs import random, plantSeeds, selectStream


class LehmerMultiStream:

    def __init__(self, seed):
        self._seed = seed
        selectStream(0)
        plantSeeds(self._seed)

    def stream(self, stream):
        selectStream(stream)

    def rnd(self):
        u = random()
        return u

    def rndn(self, n):
        sample = []
        for i in range(0, n):
            u = random()
            sample.append(u)
        return sample

def _testLehmerMultiStream():
    generator = LehmerMultiStream(1)
    generator.stream(0)
    sample = generator.rndn(10)
    print(sample)
    generator.stream(1)
    sample = generator.rndn(10)
    print(sample)

if __name__ == '__main__':
    _testLehmerMultiStream()