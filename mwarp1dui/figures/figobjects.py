#!/usr/bin/env python

from PyQt5 import QtWidgets, QtCore
import numpy as np



class Crosshairs(object):
	def __init__(self, ax):
		self.ax    = ax
		# self.hl    = ax.axhline(0, color='0.7', ls=':')
		self.vl    = ax.axvline(0, color='0.7', ls=':')
	
	def set_visible(self, visible=True):
		self.vl.set_visible(visible)
		
	
	def update(self, x, y):
		# self.hl.set_ydata([y,y])
		self.vl.set_xdata([x,x])





