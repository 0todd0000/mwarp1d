#!/usr/bin/env python

import sys,os
from math import floor,ceil,isclose
from PyQt5 import QtWidgets, QtCore, uic
import mwarp1d


class WarpControlWidgetFreeControls(QtWidgets.QWidget):
	
	amp_changed       = QtCore.pyqtSignal(int)
	applied           = QtCore.pyqtSignal()
	cancelled         = QtCore.pyqtSignal()
	center_changed    = QtCore.pyqtSignal(int)
	head_changed      = QtCore.pyqtSignal(int)
	head_tail_changed = QtCore.pyqtSignal(int)
	initiated         = QtCore.pyqtSignal()
	tail_changed      = QtCore.pyqtSignal(int)
	
	
	
	
	
	
	
	def __init__(self, *args):
		super().__init__(*args)
		fnameUI  = os.path.join( os.path.dirname(__file__), 'warp_controls.ui' )
		uic.loadUi(fnameUI, self)
		# self.mainapp = self.parent().parent()
		self.isheadtailsynced = True
		self.isexternal       = False
		
		self.widget_amp.set_properties(label='Amplitude', min=-50, max=50, step=5, value=0)
		self.widget_head.set_properties(label='Head', min=0, max=100, step=1, value=0, minlabel='min', maxlabel='max')
		self.widget_tail.set_properties(label='Tail', min=0, max=100, step=1, value=0, minlabel='min', maxlabel='max')
		self.check_syncheadtail.setChecked(True)



		self.button_initiate.clicked.connect( self.on_initiate )
		self.button_apply.clicked.connect( self.on_apply )
		self.button_cancel.clicked.connect( self.on_cancel )

		self.check_syncheadtail.stateChanged.connect( self.on_syncheadtail )

		self.slider_position.valueChanged.connect(self.on_slider_position)

		self.set_warp_enabled(False)
		self.widget_amp.valueChanged.connect(self.on_amp_changed)
		self.widget_head.valueChanged.connect(self.on_head_changed)
		self.widget_tail.valueChanged.connect(self.on_tail_changed)


	
	def get_amp(self):
		return self.widget_amp.get_value()
	def get_head(self):
		return self.widget_head.get_value()
	def get_position(self):
		return self.slider_position.value()
	def get_tail(self):
		return self.widget_tail.get_value()
		
	def get_value_dict(self):
		position = self.get_position()
		amp      = self.get_amp()
		head     = self.get_head()
		tail     = self.get_tail()
		return dict(position=position, amp=amp, head=head, tail=tail)
		
		
		
	
	def on_apply(self):
		self.set_warp_enabled(False)
		self.applied.emit()
	def on_cancel(self):
		self.set_warp_enabled(False)
		self.cancelled.emit()
	def on_initiate(self):
		self.set_warp_enabled(True)
		self.initiated.emit()
	def on_amp_changed(self, x):
		self.amp_changed.emit(x)
	def on_head_changed(self, x):
		if self.isheadtailsynced:
			self.widget_tail.set_value(x)
			self.head_tail_changed.emit(x)
		else:
			self.head_changed.emit(x)
	def on_slider_position(self, x):
		self.center_changed.emit(x)
	def on_syncheadtail(self, x):
		if x==0:
			self.isheadtailsynced = False
		else:
			self.isheadtailsynced = True
			x0 = self.widget_head.get_value()
			x1 = self.widget_tail.get_value()
			x  = round(0.5 * (x0 + x1))
			self.widget_head.set_value(x)
			self.widget_tail.set_value(x)
			
			
			
	def on_tail_changed(self, x):
		if self.isheadtailsynced:
			self.widget_head.set_value(x)
			self.head_tail_changed.emit(x)
		else:
			self.tail_changed.emit(x)
		
		
	def set_headtail_synced(self, synced=True):
		self.check_syncheadtail.setChecked(synced)
		self.isheadtailsynced = synced


	def set_values(self, position=None, amp=None, head=None, tail=None):
		if position is not None:
			self.slider_position.setValue(position)
		if amp is not None:
			self.widget_amp.set_value(amp)
		if head is not None:
			self.widget_head.set_value(head)
		if tail is not None:
			self.widget_tail.set_value(tail)

	def set_warp_enabled(self, enable=True):
		self.box_controls.setEnabled(enable)
		self.button_initiate.setEnabled(not enable)


class WarpControlWidget(WarpControlWidgetFreeControls):
	'''
	Manual, dynamically-updating control for 1D data warping.
	
	Same as WarpControlWidgetFreeControls, but coupled with with a
	ManualWarp1D object to yield for dynamically-updating, relative-
	value widgets.
	
	Position and Amplitude controls have range: [-100%, 100%]
	Head and Tail controls have range: [0, 100%]
	
	The underlying dynamic range control is handled by the ManualWarp1D class
	
	An Amplitude value of 100%, for example, is the maximum possible
	amplitude, given the current warp Position.
	
	See the ManualWarp1D documentation string for more details
	'''
	
	amp_changed       = QtCore.pyqtSignal(float)
	center_changed    = QtCore.pyqtSignal(float)
	head_changed      = QtCore.pyqtSignal(float)
	head_tail_changed = QtCore.pyqtSignal(float)
	tail_changed      = QtCore.pyqtSignal(float)
	changed           = QtCore.pyqtSignal()
	

	def __init__(self, *args):
		super().__init__(*args)
		self.warp    = None
		self.widget_amp.set_properties(label='Amplitude', min=-100, max=100, step=1, minlabel='max (-)', maxlabel='max (+)')
		

	def set_warp(self, warp):
		self.warp    = warp
		self.slider_position.setValue( 50 )
	
	
	def on_amp_changed(self, x):
		x   = 0.01 * x
		# print(x)
		self.warp.set_amp( x )
		self.amp_changed.emit(x)
		if not self.isexternal:
			self.changed.emit()
		
		

	def on_head_changed(self, x):
		r   = 0.01 * x
		self.warp.set_head( r )

		if self.isheadtailsynced:
			self.widget_tail.set_value(x)
			self.head_tail_changed.emit(r)
		else:
			self.head_changed.emit(r)
		if not self.isexternal:
			self.changed.emit()


	def on_slider_position(self, x):
		x   = 0.01 * x
		self.warp.set_center( x )
		self.center_changed.emit( x )
		if not self.isexternal:
			self.changed.emit()
		
		
	def on_tail_changed(self, x):
		r   = 0.01 * x
		self.warp.set_tail( r )

		if self.isheadtailsynced:
			self.widget_head.set_value(x)
			self.head_tail_changed.emit(r)
		else:
			self.tail_changed.emit(r)
		if not self.isexternal:
			self.changed.emit()
		
		
	def update_values_externally_changed(self):
		self.isexternal       = True
		w                     = self.warp
		self.set_values(position=100*w.center_r, amp=100*w.amp_r, head=100*w.head_r, tail=100*w.tail_r)
		self.isexternal       = False



