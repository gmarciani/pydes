import plotly.offline as py
import plotly.graph_objs as go

trace0 = go.Scatter(
    x=[1, 2, 3, 4],
    y=[10, 15, 13, 17]
)

trace1 = go.Scatter(
    x=[1, 2, 3, 4],
    y=[16, 5, 11, 9]
)

data = go.Data([trace0, trace1])

layout = go.Layout(title='Hello World')

py.plot({
    'data': data,
    'layout': layout
}, filename='out/sample-api-offline-plot.html')
