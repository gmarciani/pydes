import math
from libs.des.rvms import idfChisquare
from controls.statistics import chisquare_bivariate
import plotly.graph_objs as go
from models.demule_settings import PlotSettings


# hint: bins >= 100, len(sample) >= 10(bins^2), confidence=0.95


def observations(generator, samsize, bins):
    observed = []
    for bin1 in range(0, bins):
        observed.append([])
        for bin2 in range(0, bins):
            observed[bin1].append(0)

    for value in range(0, samsize):
        r1 = generator.rnd()
        r2 = generator.rnd()
        bin1 = math.floor(r1 * bins)
        bin2 = math.floor(r2 * bins)
        observed[bin1][bin2] += 1

    return observed


def chisquare(observed, samsize):
    bins = len(observed)
    expected = samsize / (bins ** 2)
    value = chisquare_bivariate(observed, expected)
    return value


def critical_min(bins, confidence):
    return idfChisquare((bins ** 2) - 1, (1 - confidence) / 2)


def critical_max(bins, confidence):
    return idfChisquare((bins ** 2) - 1, 1 - (1 - confidence) / 2)


def plot(data, min, max):
    streams = len(data)

    trace = go.Scatter(
        name='Random',
        x=[result[0] for result in data],
        y=[result[1] for result in data],
        mode='markers'
    )

    bound_min = go.Scatter(
        name='Min',
        x=[0, streams],
        y=[min, min],
        mode='lines'
    )

    bound_max = go.Scatter(
        name='Max',
        x=[0, streams],
        y=[max, max],
        mode='lines'
    )

    data = go.Data([trace, bound_min, bound_max])

    layout = go.Layout(
        title='Test of Bivariate Uniformity',
        font=PlotSettings.title_font,
        xaxis=dict(
            title='Streams',
            titlefont=PlotSettings.axis_font
        ),
        yaxis=dict(
            title='Chi-Square',
            titlefont=PlotSettings.axis_font
        ),
        showlegend=False,
        annotations=[
            dict(
                x=0,
                y=min,
                xref='x',
                yref='y',
                text='Min',
                showarrow=True,
                arrowhead=7,
                ax=-40,
                ay=0
            ),
            dict(
                x=0,
                y=max,
                xref='x',
                yref='y',
                text='Max',
                showarrow=True,
                arrowhead=7,
                ax=-40,
                ay=0
            )
        ]
    )

    figure = go.Figure(data=data, layout=layout)

    return figure