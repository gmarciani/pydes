from models.lehemer import Lehemer
from controls.randomness.uniformity import observations, chisquare, critical_min, critical_max, plot
import plotly.offline as py


SAMSIZE = 10000
STREAMS = 256
BINS = 1000
CONFIDENCE = 0.95

generator = Lehemer(1)

data = []
for stream in range(0, STREAMS):
    observed = observations(generator, SAMSIZE, BINS)
    chi = chisquare(observed, SAMSIZE)
    result = (stream, chi)
    data.append(result)

min = critical_min(BINS, CONFIDENCE)
max = critical_max(BINS, CONFIDENCE)

print('Critical Min: ' + str(min))
print('Critical Max: ' + str(max))
print('Values: ' + str(data))

figure = plot(data, min, max)

py.plot(figure, filename='../resources/randomness/test-uniformity.html')



