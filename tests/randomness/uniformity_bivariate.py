import numpy as np
from controls.randomness.uniformity_bivariate import chisquare_from_sample, critical_min, critical_max, plot
import plotly.offline as py


SAMSIZE = 100000
STREAMS = 256
BINS = 100
CONFIDENCE = 0.95

data = []
for stream in range(0, STREAMS):
    sample = []
    for i in range(0, SAMSIZE):
        rnd1 = np.random.uniform(0, 1)
        rnd2 = np.random.uniform(0, 1)
        sample.append((rnd1, rnd2))
    chi = chisquare_from_sample(sample, BINS)
    result = (stream, chi)
    data.append(result)

min = critical_min(BINS, CONFIDENCE)
max = critical_max(BINS, CONFIDENCE)

print('Critical Min: ' + str(min))
print('Critical Max: ' + str(max))
print('Values: ' + str(data))

figure = plot(data, min, max)

py.plot(figure, filename='../resources/randomness/test-uniformity-bivariate.html')
