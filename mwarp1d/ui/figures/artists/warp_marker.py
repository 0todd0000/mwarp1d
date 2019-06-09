#!/usr/bin/env python

from matplotlib.patches import Circle




class WarpMarker(object):
	
	def __init__(self, ax, visible=True):
		self._ypix  = 0
		self.ax     = ax
		self.center = 0, 0
		self.patch  = None
		self.radius = 5
		self._init()
		self.set_visible(False)
		self.ax.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)
		
	def _init(self):
		self.patch   = Circle((400,80), radius=20, ec='g', lw=2, fill=False, transform=self.ax.transScale)
		self.ax.add_patch( self.patch )
	
	@property
	def isvisible(self):
		return self.patch.get_visible()
		
	def initiate_warp(self, xpix, ypix):
		hpix   = self.ax.bbox.height
		ypix   = 0.5*hpix
		self.patch.set_center( (xpix, ypix) )
		self._ypix = ypix
		self.set_visible(True)

	def on_motion(self, event):
		if self.isvisible:
			self.patch.set_center((event.x, self._ypix))
	
	def set_radius(self, x):
		x0,x1  = self.ax.get_xlim()
		w      = x1 - x0
		hpix   = self.ax.bbox.height
		r      = x * hpix / w
		self.patch.set_radius( r )
	
	def set_visible(self, visible=True):
		self.patch.set_visible(visible)
	
