#!/usr/bin/env python

import sys,os
from PyQt5 import QtWidgets, QtCore, uic
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import cm
import numpy as np




class SimpleFigure(FigureCanvas):
	def __init__(self, parent=None):
		self.figure = Figure(dpi=100)
		self.ax     = self.figure.add_axes([0,0,1,1])
		super().__init__(self.figure)
		self.setParent(parent)
		super().setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		super().updateGeometry()

		self.setFocusPolicy( QtCore.Qt.ClickFocus )
		self.setFocus()


	def plot(self, y):
		self.ax.plot( y.T )
		
		
	def plot_mv(self, y):
		n = y.shape[2]
		colors = cm.jet( np.linspace(0, 1, n) )
		for i,c in enumerate(colors):
			self.ax.plot( y[:,:,i].T, color=c, lw=0.5 )
	
