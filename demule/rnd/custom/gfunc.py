def g(x, multiplier, modulus):
    q = int(modulus / multiplier)
    r = int(modulus % multiplier)
    t = int(multiplier * (x % q) - r * int(x / q))
    if (t > 0):
        return int(t)
    else:
        return int(t + modulus)