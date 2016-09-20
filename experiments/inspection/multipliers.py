"""
Experiment: find suitable FP,MC,FP/MC multipliers for a multi-stream Lehmer
pseudo-random generator.
"""

from demule.plots.multipliers import scatter
from demule.rnd.inspection import multiplier
from experiments import EXP_DIR, PLT_EXT, RES_EXT


def experiment():
    MODULUS = 127

    fp_multipliers = []
    mc_multipliers = []
    fpmc_multipliers = []

    for i in range(1, MODULUS):
        isFPM = False
        isMCM = False
        if multiplier.is_fp_multiplier(i, MODULUS):
            isFPM = True
        if multiplier.is_mc_multiplier(i, MODULUS):
            isMCM = True
        if isFPM and isMCM:
            fpmc_multipliers.append(i)
        if isFPM:
            fp_multipliers.append(i)
        elif isMCM:
            mc_multipliers.append(i)

    # Report
    report = \
        '======================================' + '\n' + \
        'INSPECTION: MULTIPLIERS               ' + '\n' + \
        '======================================' + '\n' + \
        'Modulus: %d' % (MODULUS,) + '\n' + \
        '--------------------------------------' + '\n' + \
        'FP Multipliers: %d (%.3f %%)' % (len(fp_multipliers), (len(fp_multipliers) / (MODULUS - 1)) * 100) + '\n' + \
        'MC Multipliers: %d (%.3f %%)' % (len(mc_multipliers), (len(mc_multipliers) / (MODULUS - 1)) * 100) + '\n' + \
        'FP/MC Multipliers: %d (%.3f %%)' % (len(fpmc_multipliers), (len(fpmc_multipliers) / (MODULUS - 1)) * 100) + '\n' + \
        '--------------------------------------' + '\n' + \
        'Candidates: %s' % ','.join(map(str, fpmc_multipliers)) + '\n\n'

    print(report)

    # Report on file
    filename = '%s/%s.%s' % (EXP_DIR, 'test-inspection-multipliers', RES_EXT)
    with open(filename, 'w') as resfile:
        resfile.write(report)

    # Plot
    data = (fp_multipliers, mc_multipliers, fpmc_multipliers)
    filename = '%s/%s.%s' % (EXP_DIR, 'test-inspection-multipliers', PLT_EXT)
    scatter(data, MODULUS, filename=filename)


if __name__ == '__main__':
    experiment()
