import numpy as np
from controls.randomness.uniformity import chisquare_from_sample, critical_min, critical_max
import plotly.offline as py
import plotly.graph_objs as go

SAMSIZE = 10000
STREAMS = 256
BINS = 1000
CONFIDENCE = 0.95

data = []
for stream in range(0, STREAMS):
    sample = np.random.uniform(0, 1, SAMSIZE)
    chi = chisquare_from_sample(sample, BINS)
    result = (stream, chi)
    data.append(result)

min = critical_min(BINS, CONFIDENCE)
max = critical_max(BINS, CONFIDENCE)

print('Critical Min: ' + str(min))
print('Critical Max: ' + str(max))
print('Values: ' + str(data))

trace = go.Scatter(
    name='Numpy.Uniform',
    x=[result[0] for result in data],
    y=[result[1] for result in data],
    mode='markers'
)

bound_min = go.Scatter(
    name='Min',
    x=[0, STREAMS],
    y=[min, min],
    mode='lines'
)

bound_max = go.Scatter(
    name='Max',
    x=[0, STREAMS],
    y=[max, max],
    mode='lines'
)

data = go.Data([trace, bound_min, bound_max])

layout = go.Layout(
    title='Test of Uniformity',
    xaxis={'title': 'Streams'},
    yaxis={'title': 'Chi-Square'}
)

py.plot({
    'data': data,
    'layout': layout
}, filename='../resources/randomness/test-uniformity.html')

