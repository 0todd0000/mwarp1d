
from PyQt5 import QtWidgets, QtCore
import numpy as np


class _SelectableArtist2D(QtCore.QObject):
	
	color_active    = '0.1'
	color_inactive  = '0.8'
	color_flagged   = (0.78, 0, 0.22)
	
	
	selected        = QtCore.pyqtSignal(int, float)
	
	Q               = None   #number of continuum points
	dragging        = False
	threshold       = 25     #distance threshold for selection (pixels)
	h               = None   #handle to Line2D object
	isactive        = False
	isflagged       = False
	isselectable    = True
	notify          = True   #notify of selection (standard output)
	zorder          = 0
	
	
	
	
	def __init__(self, ax, collection=None):
		super().__init__()
		self.ax         = ax
		self.ax.figure.canvas.mpl_connect('button_press_event', self.on_press)
		self.selected.connect( self.on_selected )
		self.collection = collection



	def distance2mouseclick(self, mx, my, pixels=True):
		x,y             = self.h.get_xdata(), self.h.get_ydata()
		d               = (x - mx)**2 + (y - my)**2
		i               = d.argmin()
		if pixels:
			xpix,ypix   = self.pixel_coordinates(x[i], y[i])
			mxpix,mypix = self.pixel_coordinates(mx, my)
			d           = ((xpix - mxpix)**2 + (ypix - mypix)**2 )**0.5
		else:
			d           = d.min()**0.5
		return i,d

	def get_xdata(self):
		return self.h.get_xdata()
	def get_ydata(self):
		return self.h.get_ydata()
	
	def get_ydata_normalized(self):
		y  = self.h.get_ydata()
		yn = (y-y.min()) / (y.max()-y.min())
		return yn
	
	
	@property
	def isvisible(self):
		return self.h.get_visible()
	

	def on_press(self, event):
		if self.isselectable:
			if event.button == 1 and self.isvisible:
				mx,my       = event.xdata, event.ydata  #mouse coordinates
				ind,d       = self.distance2mouseclick(mx, my)
				if d < self.threshold:
					self.selected.emit(ind, d)
				
				
	def on_selected(self, ind, distance):
		if self.notify:
			print(self.__class__.__name__ + ' selected', ind, distance)


	def pixel_coordinates(self, x, y):
		return self.ax.transData.transform( (x, y) )
		
	
	def set_active(self, active=True):
		c      = self.color_active if active else self.color_inactive
		c      = self.color_flagged if self.isflagged else c
		self.h.set_color(c)
		self.isactive = active
	
	def set_flagged(self, flagged):
		self.isflagged = flagged
	
	def set_notify(self, notify):
		self.notify     = notify
	
	def set_selectable(self, selectable=True):
		self.isselectable = selectable
	
	
	def set_visible(self, visible):
		if self.h is not None:
			self.h.set_visible(visible)

	def toggle_flag(self):
		self.isflagged = not self.isflagged
	
	
	def update_colors(self):
		if self.isflagged:
			self.h.set_color(self.color_flagged)
		elif self.isactive:
			self.h.set_color(self.color_active)
		else:
			self.h.set_color(self.color_inactive)
		self.ax.figure.canvas.draw()
		
