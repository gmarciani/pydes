from rnd.inspection.jumper_finder import find_jumper


MODULUS = 401 # 127 (8bit), 32749 (16bit), 2147483647 (32bit), 9223372036854775783 (64bit)
STREAMS = 128 # 128, 256, 512, 1024, 2048

modulus = find_jumper(MODULUS, STREAMS)

# Report
print('======================================')
print('INSPECTION: JUMPER                    ')
print('======================================')
print('Modulus: %d' % MODULUS)
print('--------------------------------------')
print('Candidate: %d' % modulus)
print('\n')