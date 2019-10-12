
import numpy as np
from matplotlib import pyplot as plt
import mwarp1d


#define warp:
Q    = 101  #domain size
warp = mwarp1d.ManualWarp1D(Q)  #constrained Gaussian kernel warp object
warp.set_center(0.25)
warp.set_amp(0.5)
warp.set_head(0.2)
warp.set_tail(0.2)

y    = np.linspace(0, 1, Q)  #an example source
yw   = warp.apply_warp(y) #warped source



#plot:
plt.close('all')
plt.figure( figsize=(6,4) )
ax = plt.axes([0.12,0.12,0.87,0.87])
ax.plot(y, label='Original')
ax.plot(yw, label='Warped')
ax.legend()
ax.set_xlabel('Domain position  (%)', size=13)
ax.set_ylabel('Dependent variable value', size=13)
plt.show()


