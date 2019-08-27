
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
pyplot.figure( figsize=(6,4) )
ax = pyplot.axes([0.12,0.12,0.87,0.87])
colors = 'r', 'g', 'b'
#plot warped domains:
ax.plot(q0, q0, 'k', lw=5)
for q,c in zip(qw,colors):
	ax.plot(q0, q, color=c)
ax.legend(['Unwarped domain', 'Warped domain 1', 'Warped domain 2', 'Warped domain 3'], loc='lower right')
ax.set_xlabel('Unwarped domain  (%)', size=13)
ax.set_ylabel('Warped domain  (%)', size=13)
pyplot.show()


# #save figure:
# dir0     = os.path.dirname(__file__)
# fnamePDF = os.path.join(dir0, 'figs', 'fig_warped_domains.pdf')
# pyplot.savefig(fnamePDF)