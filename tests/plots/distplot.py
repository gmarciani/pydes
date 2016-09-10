import plotly.offline as py
import plotly.graph_objs as go
from plotly.tools import FigureFactory as FF

import numpy as np

N = 1000
trace0 = np.random.randn(N)
trace1 = np.random.randn(N) + 2

data = [trace0, trace1]

labels = ['Trace-0', 'Trace-1']

figure = FF.create_distplot(data, labels, bin_size=[0.1, 0.2])

figure['layout'].update(title='Sample Distplot')

py.plot(figure, filename='../resources/plots/sample-distribution-plot.html')
