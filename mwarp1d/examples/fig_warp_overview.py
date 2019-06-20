
import os
import numpy as np
from matplotlib import pyplot
import mwarp1d


#load data:
dir0     = os.path.dirname(__file__)
fnameCSV = os.path.join(dir0, 'data', 'Dorn2012-1000nodes.csv')
Y        = np.loadtxt(fnameCSV, delimiter=',')
y        = Y[-1]   #example trial for demonstration


#create three different warps:
Q        = y.size  #number of continuum nodes
centers  = [0.05, 0.50, 0.75]
amps     = [0.2, 0.5, -0.8]
heads    = [0.5, 0.3, 0.5]
tails    = [0.1, 0.3, 0.5]
warps    = []
for c,a,h,t in zip(centers, amps, heads, tails):
	warp = mwarp1d.ManualWarp1D(Q)
	warp.set_center(c)
	warp.set_amp(a)
	warp.set_head(h)
	warp.set_tail(t)
	warps.append( warp )
	

#get displacement fields and warped domains:
d        = [100./Q * w.get_displacement_field()  for w in warps]
qw       = [100./Q * w.get_warped_domain()  for w in warps]
q0       = np.linspace(0, 100, Q)


#apply warps:
yw       = [w.apply_warp(y) for w in warps]


#plot:
pyplot.close('all')
pyplot.figure( figsize=(12,8) )
#create axes:
axx,axy = [0.065, 0.575], [0.55, 0.06]
axw,axh = 0.42, 0.40
ax0    = pyplot.axes([axx[0],axy[0],axw,axh])
ax1    = pyplot.axes([axx[1],axy[0],axw,axh])
ax2    = pyplot.axes([axx[0],axy[1],axw,axh])
ax3    = pyplot.axes([axx[1],axy[1],axw,axh])
colors = 'r', 'g', 'b'


#plot example pulse:
w = mwarp1d.ManualWarp1D(100)
w.set_center(0.20)
w.set_amp(0.25)
w.set_head(0.9)
w.set_tail(0.3)
dq = w.get_displacement_field()
ax0.plot(dq, color='b')
ax0.set_xlabel('Domain position  (%)', size=13)
ax0.set_ylabel('Displacement  (%)', size=13)
# label parameters:
c = w.center
ax0.plot([0,c], [0,0], color='k', ls=':')
ax0.plot([c]*2, [0,dq.max()], color='k', ls=':')
xh,xt = 14,72
ax0.plot([xh,c], [dq[xh]]*2, color='k', ls=':')
ax0.plot([c,xt], [dq[xt]]*2, color='k', ls=':')

bbox = dict(facecolor='w', edgecolor='0.7', alpha=0.9)
ax0.text(0.5*c, 0, 'center', ha='center', bbox=bbox)
ax0.text(c, 0.8*dq.max(), 'amp', ha='center', bbox=bbox)
ax0.text(0.5*(xh+c), dq[xh], 'head', ha='center', bbox=bbox)
ax0.text(c + 0.5*(xt-c), dq[xt], 'tail', ha='center', bbox=bbox)
ax0.legend(['Displacement field'])


#plot displacement fields:
for dd,c in zip(d,colors):
	ax1.plot(q0, dd, color=c)
ax1.axhline(0, color='k', ls=':')
ax1.legend(['Field 1', 'Field 2', 'Field 3'])
ax1.set_xlabel('Domain position  (%)', size=13)
ax1.set_ylabel('Displacement  (%)', size=13)

#plot warped domains:
ax2.plot(q0, q0, '0.7', lw=5)
for q,c in zip(qw,colors):
	ax2.plot(q0, q, color=c)
ax2.legend(['Unwarped domain', 'Warped domain 1', 'Warped domain 2', 'Warped domain 3'], loc='lower right')
ax2.set_xlabel('Unwarped domain  (%)', size=13)
ax2.set_ylabel('Warped domain  (%)', size=13)


#plot warped data:
ax3.plot(y, color='0.7', lw=5)
for yy,c in zip(yw,colors):
	ax3.plot(yy, color=c)
ax3.axhline(0, color='k', ls=':')
ax3.legend(['Original data', 'Warped data 1', 'Warped data 2', 'Warped data 3'], loc='lower right')
ax3.set_xlabel('Domain position  (%)', size=13)
ax3.set_ylabel('Ground reaction force  (N)', size=13)

#add panel labels:
for i,ax in enumerate([ax0,ax1,ax2,ax3]):
	ax.text(0.03, 0.92, '(%s)'%chr(97+i), size=14, transform=ax.transAxes)

pyplot.show()


# #save figure:
# fnamePDF = os.path.join(dir0, 'figs', 'fig_warp_overview.pdf')
# pyplot.savefig(fnamePDF)