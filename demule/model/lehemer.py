from lib.des.rng import random, putSeed

SEED = 1
SAMPLE_SIZE = 100

sample = []

putSeed(SEED)
for i in range(0, SAMPLE_SIZE):
    u = random()
    sample.append(u)

for i in sample:
    print(i)
