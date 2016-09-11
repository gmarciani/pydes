from libs.des.rvms import idfChisquare
from controls.statistics import get_frequencies_bivariate
import plotly.graph_objs as go


def test(sample, bins, confidence): # hint: bins >= 100, len(sample) >= 10(bins^2), confidence=0.95
    report = {}

    report['chi-square'] = chisquare_from_sample(sample, bins)
    report['critical-min'] = critical_min(bins, confidence)
    report['critical-max'] = critical_max(bins, confidence)

    return report


def chisquare_from_sample(sample, bins):
    samsize = len(sample)
    observed = get_frequencies_bivariate(sample, 0, 1, bins)
    expected = samsize / (bins ** 2)
    v = 0
    for bin1 in range(0, bins):
        for bin2 in range(0, bins):
            v += ((observed[bin1][bin2] - expected) ** 2) / expected
    return v


def critical_min(bins, confidence):
    return idfChisquare((bins ** 2) - 1, (1 - confidence) / 2)


def critical_max(bins, confidence):
    return idfChisquare((bins ** 2) - 1, 1 - (1 - confidence) / 2)


def plot(data, min, max):
    title_font = dict(
            family='Courier New, monospace',
            size=14,
            color='#7f7f7f'
    )

    axis_font = dict(
        family='Courier New, monospace',
        size=14,
        color='#7f7f7f'
    )

    streams = len(data)

    trace = go.Scatter(
        name='Numpy.Uniform',
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
        font=title_font,
        xaxis=dict(
            title='Streams',
            titlefont=axis_font
        ),
        yaxis=dict(
            title='Chi-Square',
            titlefont=axis_font
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