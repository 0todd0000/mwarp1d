#!/usr/bin/env python

import os
from PyQt5 import QtWidgets, QtCore
import numpy as np
from scipy.io import loadmat


try:
	from . message_box import MessageBox
except:
	from message_box import MessageBox



class DragDropLabel(QtWidgets.QLabel):
	
	files_dropped = QtCore.pyqtSignal(list)
	ftypes        = ['CSV']

	def __init__(self, parent):
		super().__init__(parent)
		self.setAcceptDrops(True)


	def _check_dragged(self, e):
		return e.mimeData().hasUrls() and len(e.mimeData().urls())<=1
	
	def dragEnterEvent(self, e):
		if self._check_dragged(e):
			e.accept()
			fname = e.mimeData().urls()[0].toLocalFile()
			if os.path.splitext(fname)[1][1:].upper() in self.ftypes:
				self.set_color(1)
			else:
				self.set_color(2)
		else:
			self.set_color(2)
			e.ignore()

	def dragLeaveEvent(self, e):
		self.set_color(0)
		

	def dropEvent(self, e):
		filenames = [url.toLocalFile() for url in e.mimeData().urls()]
		self.files_dropped.emit(filenames)

	def set_color(self, color_code):
		if color_code == 0:
			self.setStyleSheet('background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(150, 150, 150, 255), stop:1 rgba(200, 200, 200, 255));')
		elif color_code == 1:
			self.setStyleSheet('background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(150, 210, 150, 255), stop:1 rgba(200, 200, 200, 255));')
		else:
			self.setStyleSheet('background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(210, 150, 150, 255), stop:1 rgba(200, 200, 200, 255));')


	def set_filetypes(self, ftypes):
		self.ftypes = ftypes




class MultiFileDragDropLabel(DragDropLabel):
	
	files_dropped  = QtCore.pyqtSignal(list, str, np.ndarray)
	
	maxnumfiledict = dict(CSV=1)
	
	_accept        = False
	_checknext     = True
	_y             = np.array([])
	
	
	def _assert(self, tf, msg):
		if self._checknext:
			self._accept = tf
			if not tf:
				self._checknext = False
				MessageBox(msg)
		
	
	def _check_dragged(self, e):
		fnames  = [s.toLocalFile() for s in e.mimeData().urls()]
		exts    = [os.path.splitext(s)[1][1:].upper()  for s in fnames]
		exts    = np.array(exts)
		ext     = exts[0]

		#check that all file extensions are the same
		self._assert( np.all(exts==ext), 'All dragged files must have the same extension' )
		
		#check that all file extensions are supported
		self._assert( exts[0] in self.ftypes, '%s files unsupported.\nFile type must be one of:\n%s' %(exts[0],self.ftypes) )
		
		#check extension-specific maximum number of files
		self._assert( len(fnames) <= self.maxnumfiledict[ ext ], 'Maximum number of %s files is: %d' %(ext,self.maxnumfiledict[ext]) )


		
		#######
		# check file readability (result of each check should be a single variable "y" which will be subject to further common checks)
		#######
		
		y    = np.array([])
		
		#check NPY file:
		if self._checknext and ext == 'NPY':
			try:
				y   = np.load( fnames[0] )
			except:
				self._checknext = False
				MessageBox('NPY file unreadable.\nMust be readble using:\n  np.load')

		#check MAT file:
		if self._checknext and ext == 'MAT':
			try:
				mfile = loadmat( fnames[0] )
			except:
				self._checknext = False
				MessageBox('MAT file unreadable.\nMust be readble using:\n  scipy.io.loadmat')
				
			if self._checknext:
				keys = [s for s in mfile.keys() if not s.startswith('__')]
				b0   = 'Y' in mfile.keys()
				b1   = len(keys) == 1
				self._assert( b0 , 'MAT file must contain only a single variable called "Y".\nNo variable named "Y" found.' )
				self._assert( b1 , 'MAT file must contain only a single variable called "Y".\nOther variables found.' )
				if b0 and b1:
					y = mfile['Y']
		
		
		#check CSV file(s):
		if self._checknext and ext == 'CSV':
			if len(fnames) == 1:
				try:
					y   = np.loadtxt( fnames[0], delimiter=',' )
				except:
					self._checknext = False
					MessageBox('CSV file unreadable.\nMust be readble using:\n  np.loadtxt(filename, delimiter=",")')

			else:
				yy  = []
				for fname in fnames:
					try:
						yy.append( np.loadtxt( fname, delimiter=',' ) )
					except:
						self._checknext = False
						MessageBox('CSV file (%s) unreadable.\nMust be readble using:\nnp.loadtxt(filename, delimiter=",")' %fname)
				if self._checknext:
					shapes = [yyy.shape for yyy in yy]
					sa     = np.array(shapes)
					self._assert( np.all(sa==sa[0]) , 'All CSV files must contain the same number of columns and rows.\nArray sizes:\n%s' %shapes )
				if self._checknext:
					y   = np.dstack(yy)


		#check that data are numeric:
		if self._checknext:
			try:
				y  = np.asarray(y, dtype=float)
			except:
				self._checknext = False
				MessageBox('Data not convertable to float.')
				

		self._y         = y if self._checknext else np.array([])
		self._checknext = True
		return self._accept
	
	
	def dragEnterEvent(self, e):
		if self._check_dragged(e):
			e.accept()
			self.set_color(1)
		else:
			e.ignore()
			self.set_color(0)
	

	def dropEvent(self, e):
		filenames = [url.toLocalFile() for url in e.mimeData().urls()]
		ext       = os.path.splitext( filenames[0] )[1][1:].upper()
		self.files_dropped.emit(filenames, ext, self._y)


	def set_maxnumfiledict(self, d):
		'''
		Specify a dictionary containing extension-specific max counts
		
		Examples:
		
		d = dict(CSV=100, NPY=1, MAT=1)
		'''
		self.maxnumfiledict = d


	
	