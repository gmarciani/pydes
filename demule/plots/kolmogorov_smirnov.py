import plotly.graph_objs as go

from plots import *


def histogram(title, ksdistances, kspoint, kscritical):
    size = len(ksdistances)

    trace_ksdistances = go.Bar(
        name='KS-Distances',
        x=[value[0] for value in ksdistances],
        y=[value[1] for value in ksdistances],
        marker=dict(
            color=BLUE
        )
    )

    trace_ks = go.Bar(
        name='KS-Statistic',
        x=kspoint[0],
        y=kspoint[1],
        marker=dict(
            color=RED
        )
    )

    bound_max = go.Scatter(
        name='Critical Distance',
        x=[0, ksdistances[-1][0]],
        y=[kscritical, kscritical],
        mode='lines',
        line=dict(
            color=RED,
            width=1,
            dash='dot'
        )
    )

    data = go.Data([trace_ksdistances, trace_ks, bound_max])

    layout = go.Layout(
        title=title,
        font=TITLE_FONT,
        xaxis=dict(
            title='Chi-Square',
            titlefont=AXIS_FONT
        ),
        yaxis=dict(
            title='KS-Distance',
            titlefont=AXIS_FONT
        ),
        showlegend=False,
        annotations=[
            dict(
                x=0,
                y=kscritical,
                xref='x',
                yref='y',
                text='Critical Distance',
                showarrow=True,
                arrowhead=3,
                ax=-40,
                ay=0
            )
        ]
    )

    figure = go.Figure(data=data, layout=layout)

    return figure