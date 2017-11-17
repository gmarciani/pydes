"""
Experiment: find suitable FP,MC,FP/MC multipliers for a multi-stream Lehmer
pseudo-random generator.
"""

from demule.rnd.inspection import multiplier
from demule.utils.report import SimpleReport
from demule.plots.multipliers import scatter
from experiments import EXP_DIR, PLT_EXT, RES_EXT


_MODULUS = 127


def experiment(modulus=_MODULUS):


    fp_multipliers = []
    mc_multipliers = []
    fpmc_multipliers = []

    for i in range(1, modulus):
        isFPM = False
        isMCM = False
        if multiplier.is_fp_multiplier(i, modulus):
            isFPM = True
        if multiplier.is_mc_multiplier(i, modulus):
            isMCM = True
        if isFPM and isMCM:
            fpmc_multipliers.append(i)
        if isFPM:
            fp_multipliers.append(i)
        elif isMCM:
            mc_multipliers.append(i)

    # Report
    r = SimpleReport('MULTIPLIERS')
    r.add('General', 'Modulus', modulus)
    r.add('Multipliers', 'FP', len(fp_multipliers))
    r.add('Multipliers', 'MC', len(mc_multipliers))
    r.add('Multipliers', 'FP/MC', len(fpmc_multipliers))
    r.add('Multipliers (%)', 'FP', '%.3F' % (100 * len(fp_multipliers) / (modulus - 1)))
    r.add('Multipliers (%)', 'MC', '%.3F' % (100 * len(mc_multipliers) / (modulus - 1)))
    r.add('Multipliers (%)', 'FP/MC', '%.3F' % (100 * len(fpmc_multipliers) / (modulus - 1)))
    r.add('Result', 'Multiplier',
          fpmc_multipliers[-1] if len(fpmc_multipliers) > 0 else '-')

    r.save('%s/%s.%s' % (EXP_DIR, 'test-inspection-multipliers', RES_EXT))

    print(r)

    # Plot
    data = (fp_multipliers, mc_multipliers, fpmc_multipliers)
    filename = '%s/%s.%s' % (EXP_DIR, 'test-inspection-multipliers', PLT_EXT)
    scatter(data, modulus, filename=filename)


if __name__ == '__main__':
    experiment()
