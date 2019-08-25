#!/usr/bin/env python

import sys,os
from PyQt5 import QtWidgets, QtCore, uic
import numpy as np


def add_filename_suffix(filename, s):
	'''
	https://stackoverflow.com/questions/37487758/how-to-add-an-id-to-filename-before-extension
	'''
	return "{0}{2}.{1}".format(*filename.rsplit('.', 1) + [s])




class ApplyDialog(QtWidgets.QDialog):

	y            = None
	yw           = None


	def __init__(self, parent=None, mode='online'):
		super().__init__(parent=parent)
		fnameUI  = os.path.join( os.path.dirname(__file__), 'dialog_apply.ui' )
		uic.loadUi(fnameUI, self)
		self.panel = parent
		self.mode  = mode
		self.label_fname1.setText("")
		
		### connect:
		self.label_drop_data_files.files_dropped.connect( self.on_drop )
		self.label_fname1.clicked.connect( self.on_filename_clicked )
		self.buttonbox.accepted.connect( self.on_save )

	def on_drop(self, filenames):
		fname      = filenames[0]
		fname1     = add_filename_suffix(fname, '_w')
		self.label_fname1.setText( fname1 )

		self.y   = np.loadtxt(fname, delimiter=',')
		if self.mode=='online':
			self.yw = self.panel.data.apply_warps( self.y )
		else:
			self.yw = self.y.copy()
		self.fig.ax.plot(self.y.T)
		self.figw.ax.plot(self.yw.T)
		self.stack.setCurrentIndex(1)
		self.stackw.setCurrentIndex(1)

		self.fnamesOUT = fname


	def on_filename_clicked(self):
		print('on_filename_clicked')
	
	def on_save(self):
		dir0,s   = os.path.split(self.fnamesOUT)
		s        = s[:-4] + '_w' + s[-4:]
		fname1   = os.path.join(dir0, s)
		np.savetxt(fname1, self.yw, delimiter=',')


if __name__ == '__main__':
	app    = QtWidgets.QApplication(sys.argv)
	widget = ApplyDialog(None, 'offline')
	widget.show()
	sys.exit(app.exec_())
