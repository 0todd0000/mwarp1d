
import os
import numpy as np
from matplotlib import pyplot
import mwarp1d


#load data:
dir0     = os.path.dirname(__file__)
fnameCSV = os.path.join(dir0, 'data', 'Dorn2012.csv')
y        = np.loadtxt(fnameCSV, delimiter=',')
y0,y1    = y[0], y[-1]   #two trials for demonstration


#define landmarks and apply warp:
lm0      = [0, 9, 14, 24, 70, 99]
lm1      = [0, 11, 22, 33, 73, 99]
y1w      = mwarp1d.warp1d_landmarks(y1, lm0, lm1)


#plot:
pyplot.close('all')
pyplot.figure( figsize=(10,4) )
#create axes:
ax0 = pyplot.axes([0.08,0.12,0.42,0.84])
ax1 = pyplot.axes([0.57,0.12,0.42,0.84])
c0  = (0.3, 0.3, 0.98)
c1  = (0.98, 0.7, 0.3)
#plot data and landmarks:
h0  = ax0.plot(y0, color='0.0', lw=3)[0]
h1  = ax0.plot(y1, color='0.7', lw=1)[0]
h2  = ax0.plot(lm0[1:-1], y0[lm0[1:-1]], 'o', color=c0, ms=7)[0]
h3  = ax0.plot(lm1[1:-1], y1[lm1[1:-1]], 'o', color=c1, ms=7)[0]
ax0.legend([h0,h1,h2,h3], ['Template', 'Source', 'Template landmarks', 'Source landmarks'], loc='lower right')
#plot warped data:
h0  = ax1.plot(y0, color='0.0', lw=3)[0]
h1  = ax1.plot(y1, color='0.7', lw=1)[0]
h2  = ax1.plot(y1w, color=c1, lw=2)[0]
ax1.legend([h0,h1,h2], ['Template', 'Source', 'Warped source'], loc='lower right')
#annotate:
for ax in [ax0,ax1]:
	ax.axhline(0, color='k', ls=':')
	ax.text(70, 40, 'Medial', va='center')
	ax.text(70,-40, 'Lateral', va='center')
	ax.set_xlabel('Time  (%)', size=13)
ax0.set_ylabel('Mediolateral ground reaction force  (N)', size=13)
#add panel labels:
ax0.text(-3, 520, '(a)', size=14)
ax1.text(-3, 520, '(b)', size=14)
pyplot.show()


# #save figure:
# fnamePDF = os.path.join(dir0, 'figs', 'fig_landmarks.pdf')
# pyplot.savefig(fnamePDF)