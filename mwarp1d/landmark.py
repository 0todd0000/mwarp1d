
'''
landmark warping functions
'''

import numpy as np
from scipy import interpolate



def interp1d(y, n=101, dtype=None, kind='linear', axis=-1, copy=True, bounds_error=True, fill_value=np.nan):
	'''
	Interpolate to a fixed number of points

	:Args:
		**y** --- original 1D data (NumPy array)
		
	:Keyword args:
		**n** --- number of nodes in the interpolated vector (integer)
	
		**other arguments** --- see documentation for **scipy.interpolate.interp1d**

		

	:Returns:
		n-element NumPy array containing Gaussian half kernel
	
	:Example:
		
		>>> from matplotlib import pyplot as plt
		>>> import mwarp1d
		>>> 
		>>> k = mwarp1d.gaussian_half_kernel(10, 3, 51, reverse=True)
		>>> ki = mwarp1d.interp1d(k, 200)
		>>> 
		>>> plt.figure()
		>>> plt.plot(k, label='Original')
		>>> plt.plot(ki, label='Interpolated')
		>>> plt.legend()
		>>> plt.show()
	'''
	t0   = np.arange( y.shape[0] )
	t1   = np.linspace(0, y.shape[0]-1, n)
	f    = interpolate.interp1d(t0, y, kind, axis, copy, bounds_error, fill_value)
	y1   = f(t1)
	if dtype is not None:
		y1   = np.asarray(y1, dtype=dtype)
	return y1
	







def warp_landmark(y, x0, x1, **kwdargs):
	'''
	Warp 1D data using landmarks. Default: piecewise linear interpolation between landmarks.
	
	Landmarks must be specified as integers and must lie at least two nodes from the endpoints.
	For example, if the domain has 100 nodes, then the minimum and maximum landmark positions
	are 2 and 97, respectively.  (i.e., 0+2 and 99-2)
	
	:Args:
		**y** --- original 1D data (NumPy array)
	
		**x0** --- original landmark locations (list or array of integers, monotonically increasing)
	
		**x1** --- new landmark locations (list or array of integers, monotonically increasing)
	
	:Keyword args:
		
		(See documentation for **scipy.interpolate.interp1d**)
	
	:Example:
	
		>>> import numpy as np
		>>> from matplotlib import pyplot as plt
		>>> import mwarp1d
		>>> 
		>>> #define landmarks:
		>>> Q    = 101            #domain size
		>>> x0   = [38, 63]       #initial landmark location(s)
		>>> x1   = [25, 68]       #final landmark location(s)
		>>> 
		>>> #apply warp:
		>>> y    = np.sin( np.linspace(0, 4*np.pi, Q) )  #an arbitary 1D observation
		>>> yw   = mwarp1d.warp_landmark(y, x0, x1)   #warped 1D observation
		>>> 
		>>> #plot:
		>>> plt.figure()
		>>> ax = plt.axes()
		>>> c0,c1 = 'blue', 'orange'
		>>> ax.plot(y,  color=c0, label='Original')
		>>> ax.plot(yw, color=c1, label='Warped')
		>>> [ax.plot(xx, y[xx],  'o', color=c0)  for xx in x0]
		>>> [ax.plot(xx, yw[xx], 'o', color=c1)    for xx in x1]
		>>> ax.legend()
		>>> ax.set_xlabel('Domain position  (%)', size=13)
		>>> ax.set_ylabel('Dependent variable value', size=13)
		>>> plt.show()
	'''
	assert isinstance(y, np.ndarray), 'y must be a numpy array'
	assert y.ndim==1, 'y must be a one-dimensional numpy array'
	Q         = y.size
	
	for i,x in enumerate([x0,x1]):
		assert isinstance(x, (list,np.ndarray)), 'x%d must be a list or a numpy array' %i
		x     = np.asarray(x)
		assert x.ndim==1, 'x%d must be a list or a one-dimensional numpy array' %i
		assert np.issubdtype(x.dtype, np.integer), 'x%d must contain only integers' %i
		assert min(x)>=2, 'minimum supported value for x%d is 2' %i
		assert max(x)<Q-2, 'maximum supported value for x%d is %d' %(i, (Q-3))
	
	x0,x1       = np.asarray(x0, dtype=int), np.asarray(x1, dtype=int)
	assert x0.size==x1.size, 'x0 and x1 must contain the same number of landmarks'
	
	for i,x in enumerate([x0,x1]):
		assert np.all( np.diff(x)>0 ), 'the integers in x%d must be monotonically increasing' %i
		
	x0,x1     = list(x0), list(x1)
	
	x0        = [0] + x0 + [Q]
	x1        = [0] + x1 + [Q]
	nlm       = len(x0)      #number of landmarks
	n1        = np.diff(x1)  #inter-landmark distances
	yw        = [interp1d(y[x0[i]:x0[i+1]], n=n1[i], **kwdargs)   for i in range(nlm-1)]
	yw        = np.hstack(yw)
	return yw



def warp_landmark_gui(y, x0=[0,50,100], x1=[0,50,100], **kwdargs):
	'''
	Minimal landmark-based warping (for internal GUI use only).
	
	Users should use the **warp_landmark** function.
	
	x0 : template landmarks
	x1 : source landmarks
	'''
	x0[-1]   += 1            #pad endpoint
	x1[-1]   += 1            #pad endpoint
	nlm       = len(x0)
	n0        = np.diff(x0)
	# n0[-1]   += 1
	yw        = [interp1d(y[x1[i]:x1[i+1]], n=n0[i], **kwdargs)   for i in range(nlm-1)]
	yw        = np.hstack(yw)
	return yw



