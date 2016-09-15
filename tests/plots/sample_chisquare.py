import matplotlib.pyplot as plt
import numpy as np

samsize = 10000


data = []
u1 = np.random.uniform(0,1)
for _ in range(samsize-1):
    u2 = np.random.uniform(0,1)
    data.append((u1, u2))
    u1 = u2

x = [v[0] for v in data]
y = [v[1] for v in data]

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

ax.scatter(x, y)

#ax.set_title('Title')
ax.set_xlabel('Stream')
ax.set_ylabel('Chi-Square')

#ax.set_xlim(0.0, 1.0)
#ax.set_ylim(0.0, 1.0)
ax.set_xlabels([0, samsize-1])
ax.set_xticks(np.linspace(0, 1, 6))
ax.set_yticks(np.linspace(0, 1, 6))


ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()
ax.tick_params(axis='x', direction='out')
ax.tick_params(axis='y', length=0)
for spine in ax.spines.values():
    spine.set_position(('outward', 5))
ax.set_axisbelow(True)

fig.savefig('../resources/sample-chisquare.svg')