#!/usr/bin/env python

import sys,os
from PyQt5 import QtWidgets, QtCore, uic
import numpy as np
from scipy.io import savemat


try:
	from . message_box import MessageBox
except:
	from message_box import MessageBox



def add_filename_suffix(filename, s):
	'''
	Thank you BartoszKP!
	https://stackoverflow.com/questions/37487758/how-to-add-an-id-to-filename-before-extension
	'''
	return "{0}{2}.{1}".format(*filename.rsplit('.', 1) + [s])








class ApplyDialog(QtWidgets.QDialog):

	_checknext     = True

	y            = None
	yw           = None
	ext          = None
	fnames0      = []
	fnames1      = []
	nfiles       = 0


	def __init__(self, parent=None, mode='online'):
		super().__init__(parent=parent)
		fnameUI  = os.path.join( os.path.dirname(__file__), 'dialog_apply.ui' )
		uic.loadUi(fnameUI, self)
		self.panel = parent
		self.mode  = mode
		self.label_fname1.setText("")
		
		self.label_drop_data_files.set_filetypes( ['CSV', 'NPY', 'MAT'] )
		self.label_drop_data_files.set_maxnumfiledict( dict(CSV=100, NPY=1, MAT=1) )
		
		
		
		self.button_save   = self.buttonbox.buttons()[0]
		self.button_cancel = self.buttonbox.buttons()[1]
		self.button_save.setVisible(False)
		self.label_fname1_label.setVisible(False)
		self.label_fname1.setVisible(False)
		
		
		### connect:
		self.label_drop_data_files.files_dropped.connect( self.on_drop )
		self.buttonbox.accepted.connect( self.on_save )


	def _assert(self, tf, msg):
		if self._checknext:
			if not tf:
				self._checknext = False
				MessageBox(msg)


	def on_drop(self, fnames, ext, y):
		J0     = self.panel.data.nsources
		Q0     = self.panel.data.nnodes
		
		
		
		if y.ndim == 2:
			J,Q = y.shape
		else:
			J,Q,I = y.shape
		
		
		self._assert( J in [J0, J0+1], 'Number of dragged sources is %d.\nMust be %d or %d.' %(J, J0, J0+1))
		self._assert( Q == Q0, 'Number of domain nodes in dragged data (Q) must be the same as for the originally imported data (Q0).\nQ  = %d.\nQ0 = %d.' %(Q, Q0))
		

		if self._checknext:
			
			if self.mode=='online':
				yw = self.panel.data.apply_warps( y )
			else:
				yw = self.y.copy()

			if y.ndim == 2:
				self.fig.ax.plot(y.T)
				self.figw.ax.plot(yw.T)
			else:
				self.fig.plot_mv(y)
				self.figw.plot_mv(yw)
			
			
			
			n        = len(fnames)
			fnames1  = [add_filename_suffix(s, '_w')  for s in fnames]
			s        = fnames1[0] if (n==1) else fnames1[0] + '      (and %d others)' %(n-1)
			self.label_fname1.setText(s)
			
			
			self.button_save.setVisible(True)
			self.label_fname1_label.setVisible(True)
			self.label_fname1.setVisible(True)
			self.stack.setCurrentIndex(1)
			self.stackw.setCurrentIndex(1)
			
			
			self.ext     = ext
			self.fnames1 = fnames1
			self.y       = y
			self.yw      = yw

		
		
		self._checknext = True

	
	def on_save(self):
		if self.ext == 'NPY':
			np.save( self.fnames1[0], self.yw )
		elif self.ext == 'MAT':
			savemat( self.fnames1[0], dict(Y=self.yw), do_compression=True )
		elif self.ext == 'CSV':
			if len(self.fnames1)==1:
				np.savetxt( self.fnames1[0], self.yw, delimiter=',')
			else:
				for i,s in enumerate(self.fnames1):
					np.savetxt( s, self.yw[:,:,i], delimiter=',')

		


if __name__ == '__main__':
	app    = QtWidgets.QApplication(sys.argv)
	widget = ApplyDialog(None, 'offline')
	widget.move(0, 0)
	widget.show()
	sys.exit(app.exec_())
