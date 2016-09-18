from rnd.inspection.modulus import find_modulus


BITS = 64  # 8, 16, 32, 64

modulus = find_modulus(BITS)

# Report
print('======================================')
print('INSPECTION: MODULUS                   ')
print('======================================')
print('Bits: %d' % BITS)
print('--------------------------------------')
print('Candidate: %d' % modulus)
print('\n')