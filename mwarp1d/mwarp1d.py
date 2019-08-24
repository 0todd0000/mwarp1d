

from copy import copy,deepcopy
from math import floor,ceil
import numpy as np
from scipy import interpolate,stats




def gaussian_half_kernel(r, amp, n, reverse=False):
	'''
	Create left half of a Gaussian kernel.

	:Args:
		**r** --- kernel width (relative to n)
		
		**amp** --- kernel height
		
		**n** --- number of nodes used to represent the kernel

	:Keyword args:
		**reverse** --- set to True to return kernel's right half (default False)

	:Returns:
		n-element NumPy array containing Gaussian half kernel
	
	:Example:
		
		>>> from matplotlib import pyplot as plt
		>>> import mwarp1d
		>>> 
		>>> k = mwarp1d.gaussian_half_kernel(10, 3, 51, reverse=True)
		>>> 
		>>> plt.figure()
		>>> plt.plot(k)
		>>> plt.show()
	'''
	nk = floor(2.973 * r)   #kernel width
	s0 = 3.5 * n/nk
	g  = stats.norm.pdf( np.linspace(-s0, 0, n) )
	g  = (g - g[0]) / (g[-1] - g[0])
	g *= amp / g[-1]
	if reverse:
		g = g[::-1]
	return g



class _ManualWarp1DAbsolute(object):
	'''
	Manual warping field.

	(Do not use this class! Use the ManualWarp1D instead.)

	This warping field utlizes absolute domain units for warping parameters,
	which are dynamically updated, making it unsuitable for general use.
	'''
	
	def __init__(self, Q):
		'''
		Initialize warp.

		:Args:
			**Q** --- domain size (integer)
		'''
		self._alim  = None         #amp limits
		self._hlim  = None         #head limits
		self._qlim  = None         #center limits
		self._tlim  = None         #taillimits
		self.Q      = None         #domain size
		self.q0     = np.arange(Q) #original domain positions
		self.amp    = None         #warp amplitude 
		self.center = None         #pulse center
		self.head   = None         #head radius
		self.tail   = None         #tail radius
		self.set_domain_size(Q)
		
	
	def __repr__(self):
		s           = 'ManualWarp1D  (Domain size: %d)\n' %self.Q
		s          += '--- ABSOLUTE ------\n'
		s          += '   center    = %d\n' %self.center
		s          += '   amp       = %d\n' %self.amp
		s          += '   head      = %d\n' %self.head
		s          += '   tail      = %d\n' %self.tail
		s          += '--- LIMITS ------\n'
		s          += '   center    = (%d,%d)\n' %self._qlim
		s          += '   amp       = (%d,%d)\n' %self._alim
		s          += '   head      = (%d,%d)\n' %self._hlim
		s          += '   tail      = (%d,%d)\n' %self._tlim
		return s
	
	@staticmethod
	def _assert_lim(x, lim):
		assert x >= lim[0], 'value must be at least %d' %lim[0]
		assert x <= lim[1], 'value must be at most %d' %lim[1]

	@staticmethod
	def _abs_value(x, lim):
		x0,x1     = lim
		return x0 + x*(x1-x0)
		

	
	def _coerce_amp(self):
		if self.amp < self._alim[0]:
			self.amp = self._alim[0]
		elif self.amp > self._alim[1]:
			self.amp = self._alim[1]

	def _coerce_head(self):
		if self.head < self._hlim[0]:
			self.head = self._hlim[0]
		elif self.head > self._hlim[1]:
			self.head = self._hlim[1]

	def _coerce_tail(self):
		if self.tail < self._tlim[0]:
			self.tail = self._tlim[0]
		elif self.tail > self._tlim[1]:
			self.tail = self._tlim[1]
	
	
	def _init_param(self):
		Q              = self.Q
		Q2             = floor(Q/2)
		self._alim     = -Q2+5, Q2-5
		self._qlim     = 15, self.Q-15
		self._hlim     = 5, Q2
		self._tlim     = 5, Q2
		self.amp       = 0
		self.center    = Q2
		self.head      = 5
		self.tail      = 5
		self.q0        = np.arange(Q)
	
	def _update_hlim(self):
		Q,q,amp         = self.Q, self.center, self.amp
		if amp < 0:
			self._hlim  = max(5,abs(amp)), q
		else:
			self._hlim  = 5, q

	def _update_tlim(self):
		Q,q,amp         = self.Q, self.center, self.amp
		if amp > 0:
			self._tlim  = max(5,amp), Q-q
		else:
			self._tlim  = 5, Q-q

	
	def apply_warp(self, y):
		'''
		Apply warp to an arbitrary 1D observation.
		
		:Args:
			**y** --- a 1D NumPy array (must be same size as warp)
		
		:Returns:
			Warped y (1D NumPy array)
		'''
		x0    = self.get_original_domain()
		xw    = self.get_warped_domain()
		f     = interpolate.interp1d(xw, y, 'linear', bounds_error=False, fill_value=0)
		return f(x0)
	
	
	def copy(self):
		return deepcopy(self)
	
	
	def get_displacement_field(self):
		'''
		Get displacement field corresponding to the current warp parameters.
		
		:Returns:
			Displacement field (1D NumPy array)
		'''
		q0    = self.center
		r0    = self.head
		r1    = self.tail
		amp   = self.amp
		n0,n1 = self.center, self.Q-self.center
		w0    = gaussian_half_kernel(r0, amp, n0)
		w1    = gaussian_half_kernel(r1, amp, n1, reverse=True)
		w     = np.hstack([w0,w1])
		return w

	def get_amplim(self):
		return self._alim
	def get_centerlim(self):
		return self._qlim
	def get_headlim(self):
		return self._hlim
	def get_original_domain(self):
		return self.q0
	def get_taillim(self):
		return self._tlim

	def get_warped_domain(self):
		'''
		Get warped domain corresponding to the current warp parameters.
		
		:Returns:
			Warped domain (1D NumPy array)
		'''
		return self.q0 + self.get_displacement_field()
	
	def reset(self):
		'''
		Reset warp to the null warping field.
		
		:Affects:
			All warp parameters: "amp", "center", "head", "tail"
		'''
		self._init_param()

	def set_amp(self, x, coerce=True):
		self._assert_lim(x, self._alim)
		self.amp    = x
		self._update_hlim()  #head and tail dependent only on center, not on amp
		self._update_tlim()  #head and tail dependent only on center, not on amp
		#coerce other values:
		if coerce:
			self._coerce_head()
			self._coerce_tail()
			

	def set_center(self, x, coerce=True):
		self._assert_lim(x, self._qlim)
		self.center = round(x)
		# update limits:
		Q           = self.Q
		Q2          = floor(Q/2)  #half domain size
		dq0,dq1     = x, self.Q-x
		max0,max1   = floor(0.7*dq0), floor(0.7*dq1)
		max0,max1   = min(Q2, max0), min(Q2, max1)
		self._alim  = -max0, max1         #amp limits
		self._update_hlim()
		self._update_tlim()
		# coerce other values:
		if coerce:
			self._coerce_amp()
			self._coerce_head()
			self._coerce_tail()


	def set_domain_size(self, x):
		self.Q      = x
		self.reset()
	
	def set_head_tail(self, x0, x1):
		self.set_head(x0)
		self.set_tail(x1)

	def set_head(self, x):
		self._assert_lim(x, self._hlim)
		self.head = x

	def set_tail(self, x):
		self._assert_lim(x, self._tlim)
		self.tail = x
		






class ManualWarp1D(_ManualWarp1DAbsolute):
	'''
	A class for constructing constrained nonlinear 1D warps and applying them to univariate and multivariate 1D data.
	
	:Attributes:
	
		**Q** --- domain size (integer)
		
		**q0** --- original domain positions (1D NumpyArray)
	
		**amp** --- warp amplitude (absolute units, DO NOT MODIFY)
	
		**center** --- warp center (absolute units, DO NOT MODIFY)

		**head** --- warp head (absolute units, DO NOT MODIFY)
	
		**tail** --- warp tail (absolute units, DO NOT MODIFY)
	'''
	
	def __repr__(self):
		s           = 'ManualWarp1D  (Domain size: %d)\n' %self.Q
		s          += '--- ABSOLUTE ------\n'
		s          += '   center    = %d\n' %self.center
		s          += '   amp       = %d\n' %self.amp
		s          += '   head      = %d\n' %self.head
		s          += '   tail      = %d\n' %self.tail
		s          += '--- RELATIVE ------\n'
		s          += '   center    = %.3f\n' %self.center_r
		s          += '   amp       = %.3f\n' %self.amp_r
		s          += '   head      = %.3f\n' %self.head_r
		s          += '   tail      = %.3f\n' %self.tail_r
		s          += '--- LIMITS ------\n'
		s          += '   center    = (%d,%d)\n' %self._qlim
		s          += '   amp       = (%d,%d)\n' %self._alim
		s          += '   head      = (%d,%d)\n' %self._hlim
		s          += '   tail      = (%d,%d)\n' %self._tlim
		return s


	@staticmethod
	def _absolute_value(x, default, lim):
		x     = default if (x is None) else x
		x0,x1 = lim
		return x0 + x * (x1-x0)

	@staticmethod
	def _relative_value(x, default, lim):
		x     = default if (x is None) else x
		x0,x1 = lim
		return (x - x0) / (x1-x0)

	@property
	def amp_r(self):
		'''
		Warp amplitude (relative to its maximum possible size)
		'''
		return self._get_relative_amp()
	@property
	def center_r(self):
		'''
		Warp center (relative to its maximum possible size)
		'''
		return self._get_relative_center()
	@property
	def head_r(self):
		'''
		Warp head (relative to its maximum possible size)
		'''
		return self._get_relative_head()
	@property
	def tail_r(self):
		'''
		Warp tail (relative to its maximum possible size)
		'''
		return self._get_relative_tail()

	
	
	### relative to absolute parameter conversions:
	def _get_absolute_amp(self, x=None):
		x     = self.amp_r if (x is None) else x
		x0,x1 = self._alim
		if x >= 0:
			x = x * x1
		else:
			x = -(x * x0)
		return x
	
	def _get_absolute_center(self, x=None):
		return self._absolute_value(x, self.center_r, self._qlim)

	def _get_absolute_head(self, x=None):
		return self._absolute_value(x, self.head_r, self._hlim)

	def _get_absolute_tail(self, x=None):
		return self._absolute_value(x, self.tail_r, self._tlim)
		
		
	
	


	### absolute to relative parameter conversions
	def _get_relative_amp(self, x=None):
		x     = self.amp if (x is None) else x
		x0,x1 = self._alim
		if x >= 0:
			x = x / x1
		else:
			x = -(x / x0)
		return x

	def _get_relative_center(self, x=None):
		return self._relative_value(x, self.center, self._qlim)
	def _get_relative_head(self, x=None):
		return self._relative_value(x, self.head, self._hlim)
	def _get_relative_tail(self, x=None):
		return self._relative_value(x, self.tail, self._tlim)



	def get_params(self):
		return self.amp_r, self.center_r, self.head_r, self.tail_r


	### override parent's absolute methods:
	def set_amp(self, x, coerce=True):
		'''
		Set relative warp amplitude.
		
		:Args:
			**x** --- relative amplitude (float, -1 to +1)
		
		:Keyword args:
			**coerce** --- coerce child properties (default: True)

		:Affects:
			Child properties "head" and "tail"
		'''
		self._assert_lim(x, (-1, 1))
		if coerce:
			hr       = copy(self.head_r)
			tr       = copy(self.tail_r)
			x     = self._get_absolute_amp(x)
			super().set_amp(x, coerce=False)
			self.set_head( hr )
			self.set_tail( tr )
		else:
			x     = self._get_absolute_amp(x)
			super().set_amp(x, coerce=False)
			

	def set_center(self, x):
		'''
		Set relative warp center.
		
		:Args:
			**x** --- relative center (float, 0 to 1, where 0 and 1 represent the first and last continuum points)
		
		:Affects:
			Child properties "amp", "head" and "tail"
		'''
		self._assert_lim(x, (0, 1))
		ar       = copy(self.amp_r)
		hr       = copy(self.head_r)
		tr       = copy(self.tail_r)
		x        = self._get_absolute_center(x)
		super().set_center(x, coerce=False)
		self.set_amp( ar, coerce=False )
		self.set_head( hr )
		self.set_tail( tr )

	def set_head(self, x):
		'''
		Set relative warp head (i.e., warp kernel's leading edge)
		
		:Args:
			**x** --- relative head (float, 0 to 1)
		
		:Affects:
			(No child properties)
		'''
		self._assert_lim(x, (0, 1))
		x     = self._get_absolute_head( x )
		super().set_head(x)

	def set_tail(self, x):
		'''
		Set relative warp tail (i.e., warp kernel's trailing edge)
		
		:Args:
			**x** --- relative tail (float, 0 to 1)
		
		:Affects:
			(No child properties)
		'''
		self._assert_lim(x, (0, 1))
		x     = self._get_absolute_tail( x )
		super().set_tail(x)






class SequentialManualWarp(object):
	'''
	A class for storing applying a sequence of independent manual warps.
	
	:Properties:
	
		**Q** --- domain size (integer)
		
		**nwarps** --- number of manual warps in the sequence
	'''
	
	def __init__(self):
		self.warps    = []

	def __repr__(self):
		s  = 'SequentialManualWarp\n'
		s += '   Q         = %s\n' %self.Q
		s += '   nwarps    = %d\n' %self.nwarps
		return s
	
	
	@property
	def Q(self):
		return None if (self.nwarps==0) else self.warps[0].Q

	@property
	def nwarps(self):
		return len(self.warps)
	
	def asarray(self):
		return np.array([w.get_params() for w in self.warps])

	def append(self, warp):
		'''
		Append a warp to the existing sequence.
		
		:Args:
			**warp** --- a ManualWarp1D instance
		'''
		assert isinstance(warp, ManualWarp1D), 'warp must be a ManualWarp1D instance'
		if self.nwarps > 0:
			assert warp.Q == self.Q, 'warp domain size must match other warps in the sequence (size = %d)' %self.Q
		self.warps.append(warp)
		
	def apply_warp_sequence(self, y):
		'''
		Apply all warps sequentially.
		
		:Args:
			**y** --- a 1D numpy array (must be same size as the warps in the warp sequence)

		:Returns:
			warped 1D data (numpy array)
		'''
		yw = y.copy()
		for warp in self.warps:
			yw = warp.apply_warp(yw)
		return yw
	
	def fromarray(self):
		pass

	def reset(self):
		'''
		Reset the warp sequence (remove all warps)
		'''
		self.warps = []
		
		





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
	







def landmark_warp(y, x0, x1, **kwdargs):
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
		>>> yw   = mwarp1d.landmark_warp(y, x0, x1)   #warped 1D observation
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



def landmark_warp_gui(y, x0=[0,50,100], x1=[0,50,100], **kwdargs):
	'''
	Minimal landmark-based warping (for GUI use only).
	
	Users should use the **landmark_warp** function.
	
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













def launch_gui(data=None, mode=None, filename_results=None, filename_data=None):
	'''
	Command-line access to GUI launching.
	
	This function allows the user to bypass the initial GUI screen and proceed
	directly to the specified warping interface, thereby avoiding manual GUI setup.
	
	This function can be called from both Python and interactive Python. The GUI will
	be launched as a subprocess of the active Python kernel.
	
	:Keyword args:
		
		**data** --- a 2D NumPy array (rows = observations, columns = domain nodes)
		
		**mode** --- "landmarks" or "manual"
		
		**filename_results** --- file name (zipped NumPy format, with extension "npz") into which warping results will be saved

		**filename_data** --- CSV file name, formatted as "data" above (data or filename_data can be specified, but not both)
	'''
	import os
	narg        = 0
	
	# assert input argument types:
	if data is not None:
		assert isinstance(data, np.ndarray), '"data" must be a numpy array'
		assert data.ndim==2, '"data" must be a 2-D numpy array'
		narg   += 1
	if mode is not None:
		modes   = ['landmarks', 'manual']
		assert mode in modes, '"mode" must be "landmarks" or "manual"'
		narg   += 1
	if filename_results is not None:
		msg     = '"filename_results" must be a valid filename with the extension ".npz"'
		try:
			ext = os.path.splitext(filename_results)[1]
			assert ext == '.npz', msg
		except:
			raise ValueError(msg)
		narg   += 1
	if filename_data is not None:
		msg     = '"filename_data" must be an existing data file name with the extension ".csv"'
		try:
			ext = os.path.splitext(filename_data)[1]
			assert ext == '.csv', msg
			assert os.path.exists(filename_data), msg
		except:
			raise ValueError(msg)
		narg   += 1


	# assert patterns:
	if data is None and filename_data is None:
		assert mode is None, 'If neither "data" nor "filename_data" are specified, "mode" cannot be specified.'
		assert filename_results is None, 'If neither "data" nor "filename_data" are specified, "filename_results" cannot be specified.'

	# launch app (Pattern 0): no arguments:
	path2app  = os.path.join( os.path.dirname(__file__) , 'ui', 'main.py')
	command   = 'python %s' %path2app

	# (Pattern 0): no arguments:
	if (data is None) and (filename_data is None):
		os.system(command)

	# (Pattern 1): data specified:
	else:
		if data is not None:
			fnameCSV    = os.path.join( os.getcwd(), '_temp_mwarp1d.csv' )
			np.savetxt(fnameCSV, data, delimiter=',')
			print('mwarp1d: temporary data file written to: %s.' %fnameCSV)
			
		else:
			fnameCSV = filename_data
		command     += ' %s' %fnameCSV
		
		if mode is not None:
			command += ' %s' %mode
		if filename_results is not None:
			command += ' %s' %filename_results

		os.system(command)




class MWarpResults(object):
	def __init__(self, fnameNPZ):
		self.J        = None
		self.Q        = None
		self.fnameNPZ = fnameNPZ
		self.mode     = None
		self.fname0   = None
		self.fname1   = None
		self.y        = None   #sources (original)
		self.yw       = None   #sources (warped)
		self.y0       = None   #template
		self._parse()
		
	def __repr__(self):
		s   = 'MWarpResults\n'
		s  += '----- Overview -------------\n'
		s  += '    mode           = %s\n' %self.mode
		s  += '    nsources       = %d\n' %self.J
		s  += '    nnodes         = %d\n' %self.Q
		s  += '----- 1D Data -------------\n'
		s  += '    sources        = (%d,%d) array\n' %self.y.shape
		s  += '    sources_warped = (%d,%d) array\n' %self.yw.shape
		s  += '    template       = (%d,) array\n' %self.y0.size
		return s
		
	def _parse(self):
		with np.load(self.fnameNPZ, allow_pickle=True) as Z:
			self.mode                 = str( Z['mode'] )
			self.fname0               = str( Z['filename0'] )
			self.fname1               = str( Z['filename1'] )
			self.y0                   = Z['ydata_template']
			self.y                    = Z['ydata_sources']
			self.yw                   = Z['ydata_sources_warped']
			
			self.J                    = self.y.shape[0]
			self.Q                    = self.y0.size

			if self.mode == 'landmarks':
				pass
				# landmarks_template = Z['landmarks_template']
				# landmarks_sources  = Z['landmarks_sources']
				# landmark_labels    = [str(s) for s in Z['landmark_labels']]

			elif self.mode == 'manual':
				swparams = Z['seqwarps']
				swarps   = []
				for params in swparams:
					sw   = SequentialManualWarp()
					if params is not None:
						for p in params:
							amp,center,head,tail = p
							w = ManualWarp1D(self.Q)
							w.set_center(center)
							w.set_amp(amp)
							w.set_head(head)
							w.set_tail(tail)
							sw.append( w )
					swarps.append(sw)
				self.smwarps  = swarps

	
	def apply_warps(self, y):
		### presumes that the first row is the template
		return np.array([y[0]] + [ww.apply_warp_sequence(yy)   for ww,yy in zip(self.smwarps, y[1:])])
		


def loadnpz(fname):
	return MWarpResults(fname)
	

	
	


def manual_warp(y, center, amp, head=0.2, tail=0.2):
	'''
	Warp 1D data using landmarks. Default: piecewise linear interpolation between landmarks.
	
	Landmarks must be specified as integers and must lie at least two nodes from the endpoints.
	For example, if the domain has 100 nodes, then the minimum and maximum landmark positions
	are 2 and 97, respectively.  (i.e., 0+2 and 99-2)
	
	:Args:
		**y** --- original 1D data (NumPy array)
	
		**center** --- warp kernel center, relative to its feasible range (between 0 and 1)
	
		**amp** --- warp kernel amplitude, relative to its feasible range (between -1 and 1)
	
	:Keyword args:
		
		**head** --- warp kernel head width, relative to its feasible range (between 0 and 1)
	
		**tail** --- warp kernel tail width, relative to its feasible range (between 0 and 1)
	
	:Example:
	
		>>> from matplotlib import pyplot as plt
		>>> import mwarp1d
		>>> 
		>>> #define warp:
		>>> Q      = 101
		>>> center = 0.25
		>>> amp    = 0.5
		>>> head   = 0.2
		>>> tail   = 0.2
		>>> 
		>>> #apply warp:
		>>> y    = np.sin( np.linspace(0, 4*np.pi, Q) )  #an arbitary 1D observation
		>>> yw   = mwarp1d.manual_warp(y, center, amp, head, tail) #warped 1D observation
		>>> 
		>>> #plot:
		>>> plt.figure()
		>>> ax = plt.axes()
		>>> ax.plot(y, label='Original')
		>>> ax.plot(yw, label='Warped')
		>>> ax.legend()
		>>> ax.set_xlabel('Domain position  (%)', size=13)
		>>> ax.set_ylabel('Dependent variable value', size=13)
		>>> plt.show()
	
	'''
	
	Q    = y.size
	warp = ManualWarp1D(Q)
	warp.set_center(center)
	warp.set_amp(amp)               #relative warp amplitude (-1 to 1)
	warp.set_head(head)             #relative warp head (0 to 1)
	warp.set_tail(tail)             #relative warp tail (0 to 1)
	return warp.apply_warp(y)




	