import demule.rnd.custom.inspection as inspect


MODULUS = 401 # 127, 32749,  401, 2147483647, 9223372036854775783

fpm = 0
mcm = 0
fpmcm = 0

for i in range(1, MODULUS):
    isFPM = False
    isMCM = False
    if inspect.isFullPeriodMultiplier(i, MODULUS):
        isFPM = True
    if inspect.isModulusCompatible(i, MODULUS):
        isMCM = True
    if isFPM and isMCM:
        fpmcm += 1
        fpm += 1
        mcm += 1
    elif isFPM:
        fpm += 1
    elif isMCM:
        mcm += 1

# Report
print('======================================')
print('INSPECTION: MULTIPLIERS               ')
print('======================================')
print('Modulus: %d' % MODULUS)
print('--------------------------------------')
print('FP Multipliers: %d' % fpm)
print('MC Multipliers: %d' % mcm)
print('FP/MC Multipliers: %d' % fpmcm)
print('\n')
