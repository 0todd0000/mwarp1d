
import os
import numpy as np
from matplotlib import pyplot


#load data:
dir0     = os.path.dirname(__file__)
fnameCSV = os.path.join(dir0, 'data', 'Dorn2012.csv')
y        = np.loadtxt(fnameCSV, delimiter=',')


#plot:
pyplot.close('all')
pyplot.figure( figsize=(6,4) )
ax = pyplot.axes([0.12,0.12,0.87,0.87])
h0 = ax.plot(y[0:2].T, color='k')[0]
h1 = ax.plot(y[2:4].T, color='r')[0]
h2 = ax.plot(y[4:6].T, color='g')[0]
h3 = ax.plot(y[6:8].T, color='b')[0]
ax.legend([h0,h1,h2,h3], ['3.5 m/s', '5.2 m/s', '7.0 m/s', '9.5 m/s'])
ax.axhline(0, color='k', ls=':')
ax.text(70, 40, 'Medial', va='center')
ax.text(70,-40, 'Lateral', va='center')
ax.set_xlabel('Time  (%)', size=13)
ax.set_ylabel('Mediolateral ground reaction force  (N)', size=13)
pyplot.show()


# #save figure:
# fnamePDF = os.path.join(dir0, 'figs', 'fig_dataset.pdf')
# pyplot.savefig(fnamePDF)