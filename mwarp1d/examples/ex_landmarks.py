
import numpy as np
from matplotlib import pyplot
import mwarp1d


#define landmarks and apply warp:
Q        = 101  #domain size
lm0      = [25, 50, 75]  #template landmark positions
lm1      = [10, 30, 90]  #source landmark positions
y        = np.linspace(0, 1, Q)  #an example source
yw       = mwarp1d.warp_landmark(y, lm1, lm0)  #warped source


#plot:
pyplot.close('all')
pyplot.figure( figsize=(6,4) )
ax = pyplot.axes([0.12,0.12,0.87,0.87])
ax.plot(y, label='Original')
ax.plot(yw, label='Warped')
ax.legend()
ax.set_xlabel('Domain position  (%)', size=13)
ax.set_ylabel('Dependent variable value', size=13)
pyplot.show()


