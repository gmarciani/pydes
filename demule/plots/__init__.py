from matplotlib import rc
from matplotlib import style

#rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
rc('text', usetex=True)

style.use('grayscale')

BLACK = '0'
LGRAY = '0.75'
BLUE = '#3498DB'
RED = '#E74C3C'
GREY = '#7F7F7F'