
from math import floor


class Crosshairs(object):
	def __init__(self, ax, visible=True):
		self.ax    = ax
		self.vl    = ax.axvline(0, color='0.7', ls=':')
		self.vl.set_visible(visible)
	
	def get_xpos(self):
		x          = self.vl.get_xdata()[0]
		x          = x if self.vl.get_visible() else None
		return x

	def set_visible(self, visible=True):
		self.vl.set_visible(visible)

	def set_xdata(self, x):
		self.vl.set_xdata([x,x])



class CrosshairsManual(object):
	
	iswarpingenabled         = False
	threshold                = 25     #distance threshold for selection (pixels)
	markeredgecolor_inactive = 'r'
	markerfacecolor_inactive = 'w'
	markeredgecolor_active   = 'g'
	markerfacecolor_active   = (0.5, 1, 0.5)
	
	
	def __init__(self, ax, visible=True, y_constraint=None):
		self.Q     = None
		self.ax    = ax
		self.vl    = ax.axvline(0, color='0.7', ls=':', zorder=0)
		self.h     = ax.plot(0, 0, 'o', ms=8, zorder=4)[0]
		self.xpix  = None
		self.ypix  = None
		self.set_warp_active(False)
		self.set_visible(visible)

	
	def enable_warping(self, enable=True):
		self.iswarpingenabled = enable
		self.h.set_visible(False)
	
	
	def get_position_pixels(self):
		return self.xpix, self.ypix
	def get_x_position(self):
		return self.h.get_xdata()[0]
	def get_y_position(self):
		return self.h.get_ydata()[0]

	def get_y_position_constrained(self):
		ind = self.h.get_xdata()[0]
		return self.y_constraint[ind]
	
	
	def set_marker_color(self, color, facecolor):
		self.h.set_color( color )
		self.h.set_markerfacecolor( facecolor )

	def set_pixel_coordinates(self, x, y):
		self.xpix  = x
		self.ypix  = y
		
	
	def set_marker_visible(self, visible=True):
		self.h.set_visible( False )
		
	
	def set_warp_active(self, active=True):
		c0    = self.markeredgecolor_active if active else self.markeredgecolor_inactive
		c1    = self.markerfacecolor_active if active else self.markerfacecolor_inactive
		self.set_marker_color(c0, c1)
	

	def set_visible(self, visible=True):
		self.vl.set_visible(visible)
		self.h.set_visible(False)
	

	def set_xdata(self, x):
		self.vl.set_xdata([x,x])
		if self.y_constraint is not None:
			ind = min( max(0, floor(x)), self.Q-1)
			y   = self.y_constraint[ind]
			self.h.set_data( [ind], [y] )
		

	def set_y_constraint(self, y):
		self.Q            = y.size
		self.y_constraint = y
		self.set_xdata( self.h.get_xdata()[0] )
		

