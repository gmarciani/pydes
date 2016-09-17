from time import time

MULTIPLIER = 1
MODULUS = 9223372036854775783 # 2^63 -25, that is the greatest prime less than 2^63 -1
ISEED = 1 # could be any number in [1,MODULUS -1]

seed = int(ISEED)

def rnd():
    global seed

    Q = int(MODULUS / MULTIPLIER)
    R = int(MODULUS % MULTIPLIER)

    t = int(MULTIPLIER * (seed % Q) - R * int(seed / Q))
    if (t > 0):
        seed = int(t)
    else:
        seed = int(t + MODULUS)

    return float(seed / MODULUS)

def putSeed(x):
    global seed

    if x > 0:
        x = x % MODULUS
    else:
        x = time()
        x = x % MODULUS

    seed = int(x)

def getSeed():
    return seed