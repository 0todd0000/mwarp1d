#!/usr/bin/env python

import sys,os
from PyQt5 import QtWidgets, QtCore, uic
import numpy as np


class ApplyDialog(QtWidgets.QDialog):
	
	y            = None
	yw           = None
	
	
	def __init__(self, parent=None):
		super().__init__(parent=parent)
		fnameUI  = os.path.join( os.path.dirname(__file__), 'dialog_apply.ui' )
		uic.loadUi(fnameUI, self)
		
		
		self.label_drop_data_files.files_dropped.connect( self.on_drop )
		self.buttonbox.accepted.connect( self.on_save )

	def on_drop(self, filenames):
		self.fnameCSV = filenames[0]
		self.y   = np.loadtxt(self.fnameCSV, delimiter=',')
		self.yw  = self.y.copy()
		self.fig.ax.plot(self.y.T)
		self.figw.ax.plot(self.yw.T)
		self.stack.setCurrentIndex(1)
		self.stackw.setCurrentIndex(1)
		
		
	def on_save(self):
		dir0,s   = os.path.split(self.fnameCSV)
		s        = s[:-4] + '_w' + s[-4:]
		fname1   = os.path.join(dir0, s)
		np.savetxt(fname1, self.yw, delimiter=',')


if __name__ == '__main__':
	app    = QtWidgets.QApplication(sys.argv)
	widget = ApplyDialog()
	widget.show()
	sys.exit(app.exec_())
