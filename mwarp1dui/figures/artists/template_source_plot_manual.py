#!/usr/bin/env python

from math import floor
from PyQt5 import QtWidgets, QtCore, QtGui
import numpy as np
from . import CrosshairsManual, VerticalReference
from . import WarpMarker
from . import WarpableSource, WarpableTemplate





class TemplateSourcePlotManual(QtCore.QObject):
	
	
	
	axes_entered          = QtCore.pyqtSignal()
	curve_activated       = QtCore.pyqtSignal(int)
	warp_click_applied    = QtCore.pyqtSignal()
	warp_mouse_changed    = QtCore.pyqtSignal()
	is_unselected_visible = True
	
	
	def __init__(self, ax, Q):
		super().__init__()
		self._mxy0                 = None  #warp centroid
		self._sources0             = None
		self._sourcesw             = None
		self._warps                = None
		self.Q                     = Q
		self.active_object         = None
		self.ax                    = ax
		self.crosshairs            = CrosshairsManual(ax, visible=False)
		self.iswarpactive          = False
		self.isoriginalvisible     = False
		self.is_unselected_visible = True
		self.sources               = None
		self.template              = None
		self.warp                  = None
		self.warpmarker            = WarpMarker(self.ax)
		self.vref                  = VerticalReference(self.ax, visible=False)

		self.ax.figure.canvas.mpl_connect('axes_enter_event', self.on_axes_enter)
		self.ax.figure.canvas.mpl_connect('button_press_event', self.on_press)
		self.ax.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)
		self.ax.figure.canvas.mpl_connect('figure_leave_event', self.on_axes_leave)
		
		
	
	@property
	def J(self):
		return None if (self.sources is None) else len(self.sources)


	def apply_warp(self):
		self.iswarpactive        = False
		self.active_object.save_warp(self.warp)
		self.crosshairs.set_warp_active(False)
		self.warpmarker.set_visible(False)
		self.vref.set_visible(False)
		self.warp.reset()
		

	def cancel_warp(self):
		self.iswarpactive        = False
		self.crosshairs.set_warp_active(False)
		self.warpmarker.set_visible(False)
		self.vref.set_visible(False)
		self.active_object.revert_to_previous_warp()
		self.crosshairs.set_y_constraint( self.active_object.h.get_ydata() )
		self.warp.reset()
	
	def enable_curve_selection(self, enable=True):
		self.template.set_selectable(enable)
		[source.set_selectable(enable) for source in self.sources]
	

	def get_warp_params_from_mouse_position(self, xpix, ypix):
		#original location (pixels) (when "w" pressed)
		x0,y0        = self._mxy0
		#axis extend (pixels)
		w,h          = self.ax.bbox.width, self.ax.bbox.height
		w0,w1        = x0, w-x0
		#head-tail:
		headtail     = ypix / h
		#amplitude:
		amp          = xpix-x0
		amp          = amp/w0 if (amp<=0) else amp/w1
		head,tail    = headtail,headtail
		params       = dict(amp=amp, head=head, tail=tail)
		return params
		

	
	
	def initiate_warp_button_inititate(self, params):
		print('initiate_warp_button_inititate', params)
		
		x     = 0.01 * params['position']
		x0,x1 = self.ax.get_xlim()
		self.warp.set_center( x )
		self.warp.set_amp( 0.01 * params['amp'] )
		self.warp.set_head( 0.01 * params['head'] )
		self.warp.set_tail( 0.01 * params['tail'] )
		
		self.vref.set_x_position( x0 + x * (x1-x0) )
		
		self.iswarpactive        = True
		self.crosshairs.set_warp_active(True)
		self.vref.set_visible(True)

		mx,my        = self.crosshairs.get_position_pixels()
		self._mxy0   = mx, my
		self.warpmarker.initiate_warp( mx, my )
		self.warpmarker.set_visible(False)
		
		self.update_warp()
		
	
	def initiate_warp_key_w(self):  #called on "W" key press
		mx,my        = self.crosshairs.get_position_pixels()
		self._mxy0   = mx, my
		w,h          = self.ax.bbox.width, self.ax.bbox.height
		center       = mx / w
		self.warp.set_center(center)
		self.iswarpactive        = True
		self.crosshairs.set_warp_active(True)
		self.vref.set_x_position( self.crosshairs.get_x_position() )
		self.vref.set_visible(True)
		self.warpmarker.initiate_warp( mx, my )
		
	
	
	def on_axes_enter(self, event):
		if self.iswarpactive:
			self.crosshairs.set_visible(True)
			self.warpmarker.set_visible(True)
			self.ax.figure.canvas.draw()
			self.axes_entered.emit()

	def on_axes_leave(self, event):
		self.crosshairs.set_visible(False)
		self.warpmarker.set_visible(False)
		self.ax.figure.canvas.draw()
		
	
	
	def on_motion(self, event):
		
		if event.inaxes:
			self.crosshairs.set_visible(True)
			self.crosshairs.set_marker_visible( self.crosshairs.iswarpingenabled )
			self.crosshairs.set_xdata( event.xdata )
			self.crosshairs.set_pixel_coordinates(event.x, event.y)
			
			if self.iswarpactive:
				xpix,ypix    = event.x, event.y
				params       = self.get_warp_params_from_mouse_position(xpix, ypix)
				self.warp.set_amp( params['amp'], coerce=True )
				self.warp.set_head( params['head'] )
				self.warp.set_tail( params['tail'] )
				
				self.warp_mouse_changed.emit()
				self.update_warp()

			self.ax.figure.canvas.draw()
			
		else:
			self.crosshairs.set_visible(False)
			self.ax.figure.canvas.draw()


	def on_press(self, event):
		if self.iswarpactive:
			self.apply_warp()
			self.warp_click_applied.emit()
	
	
	
	def on_curve_selected(self, obj, x, y):
		if obj != self.active_object:
			self.set_all_active(False)

			if obj == self.template:
				self.set_template_active()
				self.curve_activated.emit( 0 )
			else:
				self.set_source_active( self.sources.index(obj) )
				self.curve_activated.emit( self.sources.index(obj)+1 )
			
			obj.set_active(True)
			self.active_object = obj
			
			self.ax.figure.canvas.draw()
			

	def on_warp_control_widget_changed(self):
		xw = self.warp.get_warped_domain()
		self.active_object.update_warped_domain(xw)
		self.vref.set_x_position( self.warp.center )
		self.ax.figure.canvas.draw()

	
	
	def reset_warp(self):
		self.active_object.reset_domain()
		self.ax.figure.canvas.draw()
	

	def set_all_active(self, active=True):
		self.template.set_active(active)
		[s.set_active(active) for s in self.sources]
		[s.set_original_visible(False) for s in self.sources]

	def set_next_selected(self):
		if self.active_object == self.template:
			self.set_source_active(0)
			self.curve_activated.emit( 1 )
		else:
			ind  = self.sources.index( self.active_object )
			if ind == self.J-1:
				self.set_template_active()
				self.curve_activated.emit( 0 )
			else:
				self.set_source_active(ind+1)
				self.curve_activated.emit( ind+2 )
		self.set_unselected_visible( self.is_unselected_visible )


	def set_previous_selected(self):
		if self.active_object == self.template:
			self.set_source_active(self.J-1)
			self.curve_activated.emit( self.J )
		else:
			ind  = self.sources.index( self.active_object )
			if ind == 0:
				self.set_template_active()
				self.curve_activated.emit(0)
			else:
				self.set_source_active(ind-1)
				self.curve_activated.emit(ind)
		self.set_unselected_visible( self.is_unselected_visible )

	def set_source_active(self, ind):
		self.set_all_active(False)
		self.sources[ind].set_active(True)
		self.sources[ind].set_original_visible( self.isoriginalvisible )
		self.crosshairs.enable_warping( True )
		self.crosshairs.set_y_constraint( self.sources[ind].h.get_ydata() )
		self.active_object   = self.sources[ind]

	def set_sources(self, y):
		if self.sources is None:
			self.sources   = []
			self._sources0 = y.copy()
			self._sourcesw = y.copy()
			self._warps    = np.zeros(y.shape)
			for yy in y:
				source = WarpableSource(self.ax, yy)
				source.set_active(False)
				source.set_notify(False)
				source.selected.connect( self.on_curve_selected )
				self.sources.append(source)

	
	def set_template(self, y):
		if self.template is None:
			self.template = WarpableTemplate(self.ax, y)
			self.crosshairs.set_y_constraint(y)
			
			self.template.selected.connect( self.on_curve_selected )
			self.template.set_notify(False)
			self.active_object = self.template


	def set_template_active(self, active=True):
		self.set_all_active(False)
		self.template.set_active()
		self.crosshairs.enable_warping( False )
		self.crosshairs.set_y_constraint( self.template.h.get_ydata() )
		self.active_object = self.template
		

	def set_unselected_visible(self, visible):
		for source in self.sources:
			if source.isactive:
				source.h.set_visible( True )
			else:
				source.h.set_visible( visible )
		
	
	def set_warp(self, warp):
		self.warp   = warp

	
	def set_warp_amp(self, x):
		self.warp.set_amp(x)
		self.update_warp()

	def toggle_original_source_visibility(self):
		self.isoriginalvisible = not self.isoriginalvisible
		self.active_object.toggle_original_source_visibility()
	
	
	
	def toggle_template_visible(self):
		print('toggle_template_visible')
		self.template.h.set_visible( not self.template.h.get_visible() )
	
	def toggle_unselected_visible(self):
		self.is_unselected_visible = not self.is_unselected_visible
		self.set_unselected_visible( self.is_unselected_visible )
	
	

	
	def update_warp(self):
		xw = self.warp.get_warped_domain()
		self.active_object.update_warped_domain(xw)



