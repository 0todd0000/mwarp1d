
from PyQt5 import QtWidgets, QtCore
from math import floor
import numpy as np
from . _base import _SelectableArtist2D



class _DraggablePoints(_SelectableArtist2D):
	
	dragged              = QtCore.pyqtSignal(object, int, int, float)
	dragging_stopped     = QtCore.pyqtSignal()
	point_added          = QtCore.pyqtSignal(int, int)
	point_deleted        = QtCore.pyqtSignal(int)
	point_delete_failed  = QtCore.pyqtSignal()
	maxpointsreached     = QtCore.pyqtSignal(int)
	
	color_active     = 0.98, 0.7, 0.3
	color_inactive   = '0.7'
	

	dragging_enabled = True
	dragging         = False
	# n               = 0    #number of points
	nmax            = 8    #maximum number of points
	selected_ind    = None
	xminmax         = None
	
	
	def __init__(self, ax, x, y_constraint=None, collection=None):
		super().__init__(ax, collection)
		self.Q            = y_constraint.size
		# self.n            = len(x)
		self.h            = self.ax.plot(x, y_constraint[x], 'o', ms=8, color=self.color_active, markeredgecolor='w', zorder=self.zorder)[0]
		self.y_constraint = y_constraint
		


		self.ax.figure.canvas.mpl_connect('button_release_event', self.on_release)
		self.ax.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)
	
	@property
	def n(self):
		return self.h.get_xdata().size

	@property
	def values(self):
		return self.h.get_xdata()
	
	
	def add_point(self, x):
		if self.n < self.nmax:
			y       = self.y_constraint[x]
			x0,y0   = self.get_point_coordinates()
			x0,y0   = np.append(x0, x), np.append(y0, y)
			ind     = np.argsort(x0)
			self.set_point_coordinates(x0[ind], y0[ind])
			# self.n += 1
			self.ax.figure.canvas.draw()
			col     = x0[ind].tolist().index(x)
			self.point_added.emit(col, x)
		else:
			self.maxpointsreached.emit(self.nmax)

		
	def delete_point(self, ind):
		deleted      = False
		if self.n > 1:
			x,y      = self.get_point_coordinates()
			x        = np.hstack((x[:ind], x[ind+1:]))
			y        = np.hstack((y[:ind], y[ind+1:])) 
			self.set_point_coordinates(x, y)
			deleted  = True
			self.point_deleted.emit(ind)
			self.ax.figure.canvas.draw()
		else:
			self.point_delete_failed.emit()
		return deleted
	
	def get_point_coordinates(self):
		x,y   = self.h.get_xdata(), self.h.get_ydata()
		return x,y
	
	def get_previous_point(self, ind):
		return None if (ind==0) else (ind-1)
	def get_previous_x(self, ind0):
		ind          = self.get_previous_point(ind0)
		return None if (ind is None) else self.h.get_xdata()[ind]

	def get_next_point(self, ind):
		return None if (ind==(self.n-1)) else (ind+1)
	def get_next_x(self, ind0):
		ind          = self.get_next_point(ind0)
		return None if (ind is None) else self.h.get_xdata()[ind]

	def get_xminmax(self, ind):
		x0,x1    = self.get_previous_x(ind), self.get_next_x(ind)
		x0       = 2 if (x0 is None) else x0+2
		x1       = self.Q-3 if (x1 is None) else x1-2
		return x0,x1
	
	
	
	def on_motion(self, event):
		if event.inaxes:
			
		# 	# self.crosshairs.update(x, y)
			if self.dragging_enabled and self.dragging:
				ind   = self.selected_ind
				x     = floor(event.xdata)
				x0,x1 = self.xminmax
				x     = min(x1, max(x0, x))
				y     = self.y_constraint[x]
				self.set_data(ind, x, y)
				self.dragged.emit(self, ind, x, y)
	


	
	def on_selected(self, ind, distance):
		super().on_selected(ind, distance)
		self.dragging     = True
		self.selected_ind = ind
		self.xminmax      = self.get_xminmax(ind)

	
	
	def on_release(self, event):
		self.dragging_stopped.emit()
		self.dragging     = False
		self.selected_ind = None
		self.xminmax      = None
		
		
		
	
	
	def set_active(self, active):
		super().set_active(active)
		self.isselectable = active
		
	def set_all_xdata(self, x):
		self.h.set_xdata(x)
		self.h.set_ydata( self.y_constraint[x] )

	def set_data(self, ind, xnew, ynew):
		x,y    = self.h.get_xdata(), self.h.get_ydata()
		x[ind] = xnew
		y[ind] = ynew
		self.h.set_xdata(x)
		self.h.set_ydata(y)
	
	def set_dragging_enabled(self, enabled):
		self.dragging_enabled = enabled
	
	def set_point_coordinates(self, x, y):
		self.h.set_xdata(x)
		self.h.set_ydata(y)



class SourceLandmarks(_DraggablePoints):
	color_active    = 0.98, 0.7, 0.3
	zorder          = 1
	
	def set_active(self, active):
		super().set_active(active)
		self.h.set_visible(active)
	

class TemplateLandmarks(_DraggablePoints):
	color_active    = 0.3, 0.3, 0.98
	zorder          = 3
	


