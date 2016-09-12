import plotly.graph_objs as go

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

blue='#3498DB'
red='#E74C3C'


def scatter(title, data, mn, mx):
    streams = len(data)

    data_in = [v for v in data if mn <= v[1] <= mx]

    data_out = [v for v in data if v[1] < mn or v[1] > mx]

    trace_in = go.Scatter(
        name='Random_In',
        x=[result[0] for result in data_in],
        y=[result[1] for result in data_in],
        mode='markers',
        marker=dict(
            color=(blue)
        )
    )

    trace_out = go.Scatter(
        name='Random_Out',
        x=[result[0] for result in data_out],
        y=[result[1] for result in data_out],
        mode='markers',
        marker=dict(
            color=(red)
        )
    )

    bound_min = go.Scatter(
        name='Min',
        x=[0, streams],
        y=[mn, mn],
        mode='lines',
        line=dict(
            color=(red),
            width=1,
            dash='dot'
        )
    )

    bound_max = go.Scatter(
        name='Max',
        x=[0, streams],
        y=[mx, mx],
        mode='lines',
        line=dict(
            color=(red),
            width=1,
            dash='dot'
        )
    )

    data = go.Data([trace_in, trace_out, bound_min, bound_max])

    layout = go.Layout(
        title=title,
        font=title_font,
        xaxis=dict(
            title='Streams',
            titlefont=axis_font,
            autotick=False,
            tick0=0,
            dtick=streams-1
        ),
        yaxis=dict(
            title='Chi-Square',
            titlefont=axis_font
        ),
        showlegend=False,
        annotations=[
            dict(
                x=0,
                y=mn,
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
                y=mx,
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