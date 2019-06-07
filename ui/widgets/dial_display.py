#!/usr/bin/env python

import sys,os
from PyQt5 import QtWidgets, uic



class DialDisplayWidget(QtWidgets.QWidget):
	def __init__(self, *args):
		super().__init__(*args)
		fnameUI  = os.path.join( os.path.dirname(__file__), 'dial_display.ui' )
		uic.loadUi(fnameUI, self)
		self.valueChanged  = self.dial.valueChanged
		
	def get_value(self):
		return self.dial.value()
	
	def set_label(self, s):
		self.box.setTitle(s)

	def set_minimum(self, x):
		self.dial.setMinimum(x)
		self.label_min.setText(str(x))

	def set_maximum(self, x):
		self.dial.setMaximum(x)
		self.label_max.setText(str(x))
		
	def set_maxlabel(self, s):
		self.label_max.setText(s)

	def set_minmax(self, x0, x1):
		self.set_minimum(x0)
		self.set_maximum(x1)

	def set_minlabel(self, s):
		self.label_min.setText(s)

	def set_properties(self, label='My Widget', min=-10, max=10, step=1, value=0, minlabel=None, maxlabel=None):
		self.set_label(label)
		self.set_minimum(min)
		self.set_maximum(max)
		self.set_step(step)
		self.set_value(value)
		if minlabel is not None:
			self.set_minlabel(minlabel)
		if maxlabel is not None:
			self.set_maxlabel(maxlabel)
	
	def set_step(self, x):
		self.dial.setSingleStep(x)
	
	def set_value(self, x):
		self.dial.setValue(x)

		
	def value(self):
		return self.dial.value()



