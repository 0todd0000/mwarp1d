
import os
import numpy as np
from matplotlib import pyplot
import mwarp1d


#load data:
dir0     = os.path.dirname(__file__)
fnameCSV = os.path.join(dir0, 'data', 'Dorn2012.csv')
Y        = np.loadtxt(fnameCSV, delimiter=',')
y        = Y[-1]   #example trial for demonstration


#define landmarks and apply warp:
Q        = y.size
q        = np.linspace(0, 100, Q)


warp     = mwarp1d.ManualWarp1D(y.size)
warp.set_center(0.75)
warp.set_amp(-0.2)
warp.set_head(0.5)
warp.set_tail(0.5)
yw       = warp.apply_warp(y)

d        = warp.get_displacement_field()
tw       = warp.get_warped_domain()

#plot:
pyplot.close('all')
pyplot.figure( figsize=(10,4) )
#create axes:
ax0 = pyplot.axes([0.08,0.12,0.42,0.84])

ax0.plot(q, y)
ax0.plot(q, yw)

# ax1 = pyplot.axes([0.57,0.12,0.42,0.84])
# c0  = (0.3, 0.3, 0.98)
# c1  = (0.98, 0.7, 0.3)
# #plot data and landmarks:
# h0  = ax0.plot(y0, color='0.0', lw=3)[0]
# h1  = ax0.plot(y1, color='0.7', lw=1)[0]
# h2  = ax0.plot(lm0[1:-1], y0[lm0[1:-1]], 'o', color=c0, ms=7)[0]
# h3  = ax0.plot(lm1[1:-1], y1[lm1[1:-1]], 'o', color=c1, ms=7)[0]
# ax0.legend([h0,h1,h2,h3], ['Template', 'Source', 'Template landmarks', 'Source landmarks'], loc='lower right')
# #plot warped data:
# h0  = ax1.plot(y0, color='0.0', lw=3)[0]
# h1  = ax1.plot(y1, color='0.7', lw=1)[0]
# h2  = ax1.plot(y1w, color=c1, lw=2)[0]
# ax1.legend([h0,h1,h2], ['Template', 'Source', 'Warped source'], loc='lower right')
# #annotate:
# for ax in [ax0,ax1]:
# 	ax.axhline(0, color='k', ls=':')
# 	ax.text(70, 40, 'Medial', va='center')
# 	ax.text(70,-40, 'Lateral', va='center')
# 	ax.set_xlabel('Time  (%)', size=13)
# ax0.set_ylabel('Mediolateral ground reaction force  (N)', size=13)
# #add panel labels:
# ax0.text(-3, 520, '(a)', size=14)
# ax1.text(-3, 520, '(b)', size=14)
pyplot.show()


# #save figure:
# fnamePDF = os.path.join(dir0, 'figs', 'fig2.pdf')
# pyplot.savefig(fnamePDF)