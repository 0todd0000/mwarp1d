
__version__ = '0.0.1'   #(2019.06.07)

from copy import copy
from math import floor,ceil
import numpy as np
from scipy import interpolate,stats

from mwarp1dui import launch_gui



def gaussian_half_kernel(r, amp, n, reverse=False):
	nk           = floor(2.973 * r)   #kernel width
	s0           = 3.5 * n/nk
	g            = stats.norm.pdf( np.linspace(-s0, 0, n) )
	g            = (g - g[0]) / (g[-1] - g[0])
	g           *= amp / g[-1]
	if reverse:
		g = g[::-1]
	return g



class ManualWarp1DAbsolute(object):
	
	def __init__(self, Q):
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
		x0    = self.get_original_domain()
		xw    = self.get_warped_domain()
		f     = interpolate.interp1d(xw, y, 'linear', bounds_error=False, fill_value=0)
		return f(x0)
	
	def get_displacement_field(self):
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
		return self.q0 + self.get_displacement_field()
	
	def reset(self):
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
		






class ManualWarp1D(ManualWarp1DAbsolute):
	
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
		return self._get_relative_amp()
	@property
	def center_r(self):
		return self._get_relative_center()
	@property
	def head_r(self):
		return self._get_relative_head()
	@property
	def tail_r(self):
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


	### override parent's absolute methods:
	def set_amp(self, x, coerce=True):
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
		self._assert_lim(x, (0, 1))
		x     = self._get_absolute_head( x )
		super().set_head(x)

	def set_tail(self, x):
		self._assert_lim(x, (0, 1))
		x     = self._get_absolute_tail( x )
		super().set_tail(x)





def interp1d(y, n=101, dtype=None, kind='linear', axis=-1, copy=True, bounds_error=True, fill_value=np.nan):
	t0   = np.arange( y.shape[0] )
	t1   = np.linspace(0, y.shape[0]-1, n)
	f    = interpolate.interp1d(t0, y, kind, axis, copy, bounds_error, fill_value)
	y1   = f(t1)
	if dtype is not None:
		y1   = np.asarray(y1, dtype=dtype)
	return y1
	

def warp1d_landmarks(y, x0=[0,50,101], x1=[0,50,101], **kwdargs):
	nlm       = len(x0)  #number of landmarks
	n0        = np.diff(x0)
	n0[-1]   += 1
	yw        = [interp1d(y[x1[i]:x1[i+1]], n=n0[i], **kwdargs)   for i in range(nlm-1)]
	yw        = np.hstack(yw)
	return yw



