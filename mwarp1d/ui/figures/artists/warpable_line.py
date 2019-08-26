
from PyQt5 import QtWidgets, QtCore
import numpy as np
from . _base import _SelectableArtist2D
import mwarp1d



class _WarpableLine(_SelectableArtist2D):
	linewidth          = 0.5
	iswarpable         = True
	selected           = QtCore.pyqtSignal(object, int, float)
	warp_initiated     = QtCore.pyqtSignal(object, int)
	
	
	def __init__(self, ax, y):
		super().__init__(ax, None)
		self.Q        = y.size
		self.x0       = np.arange(self.Q)  #original (unwarped) domain
		self.y0       = y                  #original (unwarped) data
		self.xw       = self.x0.copy()     #current warped domain
		self.yw       = y.copy()           #current warped data (updated only after saving warp)
		self.seqw     = mwarp1d.SequentialManualWarp()
		self.h0       = self.ax.plot(y, ':', lw=2, color=(0.8,0.3,0.3), zorder=self.zorder-1)[0]   #original, unwarped curve
		self.h        = self.ax.plot(y, '-', lw=self.linewidth, color=self.color_active, zorder=self.zorder)[0]  #current warped curve
		self.h0.set_visible(False)
	
	def on_press(self, event):
		if self.isselectable:
			if event.button == 1 and self.isvisible:
				mx,my       = event.xdata, event.ydata  #mouse coordinates
				ind,d       = self.distance2mouseclick(mx, my)
				if d < self.threshold:
					self.isselected = True
					self.selected.emit(self, ind, d)
				else:
					self.isselected = False

	def reset_domain(self):
		self.h.set_xdata(self.x0)
		self.h.set_ydata(self.y0)
		self.xw    = self.x0.copy()
		self.yw    = self.y0.copy()
		self.seqw.reset()

	def revert_to_previous_warp(self):
		self.set_warped_domain( self.xw )
		# self.xw    = self.x0.copy()

	def save_warp(self, warp):
		self.xw    = self.x0.copy()
		self.yw    = warp.apply_warp( self.h.get_ydata().copy() )
		self.seqw.append(warp.copy())
		self.h.set_xdata( self.xw )
		self.h.set_ydata( self.yw )
		
		
	
	def set_original_visible(self, visible=True):
		self.h0.set_visible(visible)
	
	def set_warped_domain(self, x):
		self.h.set_xdata(x)
		
	def set_warped_ydata(self, y):
		self.yw        = y
		self.h.set_ydata(y)
		# print('okok')

	def toggle_original_source_visibility(self):
		self.h0.set_visible( not self.h0.get_visible() )
	
	def update_warped_domain(self, xw):
		xw_new = self.xw  + (xw - self.x0)
		self.set_warped_domain( xw_new )



class WarpableSource(_WarpableLine):
	linewidth          = 0.5
	zorder             = 0
	
	def calculate_mse(self, template, normalized=True):
		if normalized:
			y0 = template.get_ydata_normalized()
			y  = self.get_ydata_normalized()
		else:
			y0 = template.h.get_ydata()
			y  = self.h.get_ydata()
		return ((y-y0)**2).mean()



class WarpableTemplate(_WarpableLine):
	iswarpable         = False
	linewidth          = 5
	zorder             = 2



	