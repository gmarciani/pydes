from time import time

MULTIPLIER = 48271
MODULUS = 9223372036854775783 # 2^63 -25, that is the greatest prime less than 2^63 -1
ISEED = 1 # could be any number in [1,MODULUS -1]
STREAMS = 256
JUMPER = 22925

seed = [int(ISEED)] * STREAMS
stream = 0
init = False


def rnd():
    global seed

    Q = int(MODULUS / MULTIPLIER)
    R = int(MODULUS % MULTIPLIER)

    t = int(MULTIPLIER * (seed % Q) - R * int(seed / Q))
    if t > 0:
        seed[stream] = int(t)
    else:
        seed[stream] = int(t + MODULUS)

    return float(seed[stream] / MODULUS)


def put_seed(x):
    global seed
    if x > 0:
        x = x % MODULUS
    else:
        x = time()
        x = x % MODULUS
    seed[stream] = int(x)


def get_seed():
    return seed[stream]


def select_stream(id):
    global stream
    stream = id % STREAMS
    if not init and stream != 0:
        plant_seeds(ISEED)


def plant_seeds(x):
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
    if (x > 0):
      seed[j] = x
    else:
      seed[j] = x + MODULUS