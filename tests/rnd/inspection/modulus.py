from rnd.inspection.modulus_finder import find_modulus


def _test():
    BITS = 8  # 8, 16, 32, 64

    modulus = find_modulus(BITS)

    # Report
    print('======================================')
    print('INSPECTION: MODULUS                   ')
    print('======================================')
    print('Bits: %d' % BITS)
    print('--------------------------------------')
    print('Candidate: %d' % modulus)
    print('\n')

if __name__ == '__main__':
    _test()