from demule.rnd.custom.modulus import find_modulus
from time import time


BITS = 64  # 8, 16, 32, 64

s = time()
modulus = find_modulus(BITS)
e = time()

print(e - s)
# Report
print('======================================')
print('INSPECTION: MODULUS                   ')
print('======================================')
print('Bits: %d' % BITS)
print('--------------------------------------')
print('Candidate: %d' % modulus)
print('\n')