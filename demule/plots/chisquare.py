from plots import *
import matplotlib.pyplot as plt


def scatter(title, data, mn, mx):
    streams = len(data)

    data_in = [v for v in data if mn <= v[1] <= mx]

    data_out = [v for v in data if v[1] < mn or v[1] > mx]

    plt.scatter(
        label='Success',
        x=[result[0] for result in data_in],
        y=[result[1] for result in data_in],
        color='blue'
    )

    plt.scatter(
        label='Failure',
        x=[result[0] for result in data_out],
        y=[result[1] for result in data_out],
        color='red'
    )

    plt.axhline(y=mn, color='red', linestyle='dashed')
    plt.axhline(y=mx, color='red', linestyle='dashed')

    plt.suptitle(title)
    plt.xlabel('Streams')
    plt.ylabel('Chi-Square')
    plt.xlim(0, streams -1)

    plt.show()