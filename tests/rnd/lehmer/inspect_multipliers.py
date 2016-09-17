from demule.rnd.custom.multiplier import is_fp_multiplier, is_mc_multiplier


MODULUS = 9223372036854775783 # 127 (8bit), 32749 (16bit), 2147483647 (32bit), 9223372036854775783 (64bit)

fp_multipliers = []
mc_multipliers = []
fpmc_multipliers = []

for i in range(1, MODULUS):
    isFPM = False
    isMCM = False
    if is_fp_multiplier(i, MODULUS):
        isFPM = True
    if is_mc_multiplier(i, MODULUS):
        isMCM = True
    if isFPM and isMCM:
        fpmc_multipliers.append(i)
    if isFPM:
        fp_multipliers.append(i)
    elif isMCM:
        mc_multipliers.append(i)

# Report
print('======================================')
print('INSPECTION: MULTIPLIERS               ')
print('======================================')
print('Modulus: %d' % MODULUS)
print('--------------------------------------')
print('FP Multipliers: %d (%.3f %%)' % (len(fp_multipliers), (len(fp_multipliers) / (MODULUS - 1)) * 100))
print('MC Multipliers: %d (%.3f %%)' % (len(mc_multipliers), (len(mc_multipliers) / (MODULUS - 1)) * 100))
print('FP/MC Multipliers: %d (%.3f %%)' % (len(fpmc_multipliers), (len(fpmc_multipliers) / (MODULUS - 1)) * 100))
print('--------------------------------------')
print('Candidates: %s' % ','.join(map(str, fpmc_multipliers)))
print('\n')
