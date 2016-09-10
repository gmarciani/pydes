from controls.statistics import get_frequencies

import numpy as np

N = 10
sample = np.random.uniform(0, 1, N)

frequencies = get_frequencies(sample, 0.0, 1.0, 10)

print(frequencies)
