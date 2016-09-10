import plotly.offline as py
import plotly.graph_objs as go

import numpy as np

N = 1000
random_x = np.random.randn(N)
random_y = np.random.randn(N)

trace = go.Scatter(
    x = random_x,
    y = random_y,
    mode = 'markers'
)

data = go.Data([trace])

layout = go.Layout(title='Sample Scatterplot')

py.plot({
    'data': data,
    'layout': layout
}, filename='out/sample-scatter-plot.html')