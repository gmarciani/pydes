from rnd.inspection.jumper_finder import find_jumper


def _test():
    MODULUS = 2147483647  # 127 (8bit), 32749 (16bit), 2147483647 (32bit), 9223372036854775783 (64bit)
    MULTIPLIER = 48271  # -, -, 48271, -
    STREAMS = 256  # 256, 512, 1024, 2048

    jumper, jumpsize = find_jumper(MODULUS, MULTIPLIER, STREAMS)

    # Report
    print('======================================')
    print('INSPECTION: JUMPER                    ')
    print('======================================')
    print('Modulus: %d' % MODULUS)
    print('Multiplier: %d' % MULTIPLIER)
    print('Streams: %d' % STREAMS)
    print('--------------------------------------')
    print('Candidate: %d' % jumper)
    print('Jump Size: %d' % jumpsize)
    print('\n')


if __name__ == '__main__':
    _test()