
import os
import numpy as np
from matplotlib import pyplot
import mwarp1d


#create three different warps:
Q        = 101   #number of continuum nodes
centers  = [0.15, 0.50, 0.75]
amps     = [0.2, 0.5, -0.6]
heads    = [0.5, 0.5, 0.5]
tails    = [0.5, 0.5, 0.5]
warps    = []
for c,a,h,t in zip(centers, amps, heads, tails):
	warp = mwarp1d.ManualWarp1D(Q)
	warp.set_center(c)
	warp.set_amp(a)
	warp.set_head(h)
	warp.set_tail(t)
	warps.append( warp )
	

#get displacement fields and warped domains:
d        = [w.get_displacement_field()  for w in warps]
qw       = [w.get_warped_domain()  for w in warps]
q0       = warps[0].get_original_domain()


#plot:
pyplot.close('all')
pyplot.figure( figsize=(10,4) )
#create axes:
ax0    = pyplot.axes([0.065,0.12,0.42,0.84])
ax1    = pyplot.axes([0.575,0.12,0.42,0.84])
colors = 'r', 'g', 'b'
#plot warped domains:
ax0.plot(q0, q0, 'k', lw=5)
for q,c in zip(qw,colors):
	ax0.plot(q0, q, color=c)
ax0.legend(['Unwarped domain', 'Warped domain 1', 'Warped domain 2', 'Warped domain 3'], loc='lower right')
ax0.set_xlabel('Unwarped domain  (%)', size=13)
ax0.set_ylabel('Warped domain  (%)', size=13)
#plot displacement fields:
for dd,c in zip(d,colors):
	ax1.plot(dd, color=c)
ax1.axhline(0, color='k', ls=':')
ax1.legend(['Field 1', 'Field 2', 'Field 3'])
ax1.set_xlabel('Domain position  (%)', size=13)
ax1.set_ylabel('Displacement  (%)', size=13)
#add panel labels:
ax0.text(0.03, 0.92, '(a)', size=14, transform=ax0.transAxes)
ax1.text(0.03, 0.92, '(b)', size=14, transform=ax1.transAxes)
pyplot.show()


#save figure:
dir0     = os.path.dirname(__file__)
fnamePDF = os.path.join(dir0, 'figs', 'fig3.pdf')
pyplot.savefig(fnamePDF)