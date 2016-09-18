def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def isprime(n):
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    max = n**0.5 + 1
    i = 3
    while i <= max:
        if n % i == 0:
            return False
        i += 2
    return True