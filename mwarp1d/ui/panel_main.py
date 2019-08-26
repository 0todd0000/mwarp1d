#!/usr/bin/env python

import sys,os
from PyQt5 import QtWidgets, QtCore, uic
import numpy as np
from widgets import FileSaveDialog,MessageBox
import dataio


class MainPanel(QtWidgets.QWidget):
	def __init__(self, parent=None):
		super().__init__(parent=parent)
		fnameUI  = os.path.join( os.path.dirname(__file__), 'panel_main.ui' )
		uic.loadUi(fnameUI, self)
		self.fname           = None    #data file name
		self.fname1          = None    #results file name
		self.mainapp         = parent
		self.template_array  = None
		self.sources_array   = None
		
		self.stackedwidget.setCurrentIndex(0)
		self.groupbox_warping_mode.setEnabled(False)
		self.label_drop_data_files.set_filetypes( ['CSV', 'NPZ'] )


		### connect callbacks:
		self.button_clear.clicked.connect(self.on_button_clear)
		self.button_landmarks.clicked.connect(self.on_button_landmarks)
		self.button_manual.clicked.connect(self.on_button_manual)
		self.label_drop_data_files.files_dropped.connect( self.on_drop )
		self.label_filename_results.clicked.connect( self.on_button_filename )
		
	
	def _plot(self):
		y0 = self.template_array
		y  = self.sources_array
		ax = self.fig.ax
		h0 = ax.plot( y0,  lw=5, color='k')[0]
		h1 = ax.plot( y.T, lw=1, color='0.8')[0]
		ax.legend([h0,h1], ['Template','Source'])
		ax.figure.canvas.draw()
		
		
		
	def on_button_clear(self):
		self.reset_panel()
		
		
	
	def on_button_filename(self):
		fname  = None
		dialog = FileSaveDialog('npz')
		dialog.setDirectory( os.path.dirname(self.fname1) )
		dialog.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)
		s      = os.path.split( self.fname1 )[-1]
		dialog.selectFile( s )
		if dialog.exec_() == QtWidgets.QDialog.Accepted:
			fname  = dialog.selectedFiles()[0]
		if fname is not None:
			self.fname1 = fname
			self.label_filename_results.setText( fname )
		return fname
	
	def on_button_landmarks(self):
		self.mainapp.start_landmark_mode(self.template_array, self.sources_array, self.fname, self.fname1)

	def on_button_manual(self):
		self.mainapp.start_manual_mode(self.template_array, self.sources_array, self.fname, self.fname1)

	def on_drop(self, filenames):
		success = False
		nfiles  = len(filenames)
		if nfiles==1:
			fname = filenames[0]
			ext   = os.path.splitext(fname)[1]
			self.mainapp.set_default_directory(  os.path.dirname(fname)  )
			if ext=='.csv':
				fname1 = self.mainapp.get_results_filename(fname)
				y      = np.loadtxt(fname, delimiter=',')
				y0,y   = y[0], y[1:]
				

				self.fname          = fname
				self.fname1         = fname1
				self.template_array = y0
				self.sources_array  = y
				self._plot()
				self.label_nsources.setText( str(y.shape[0]) )
				self.label_nnodes.setText( str(y0.size) )

				self.label_filename_results.setText( fname1 )
				success = True

			elif ext=='.npz':
				data = dataio.loadnpz(fname)
				self.start_npz(data)
			else:
				MessageBox('Error: only csv and npz')
				self.label_drop_data_files.set_color(0)

		if success:
			self.stackedwidget.setCurrentIndex(1)
			self.groupbox_warping_mode.setEnabled(True)

		
	def reset_panel(self):
		self.label_filename_results.setText( "" )
		self.label_nsources.setText( "" )
		self.label_nnodes.setText( "" )
		self.groupbox_warping_mode.setEnabled(False)
		self.label_drop_data_files.reset_color()
		
		self.fname          = None
		self.fname1         = None
		self.template_array = None
		self.sources_array  = None
		
		self.fig.reset()
		
		self.stackedwidget.setCurrentIndex(0)
	
	
	def set_fname_results(self, s):
		self.fname1         = s
		self.label_filename_results.setText( s )
		
	
	def start_npz(self, data):
		self.mainapp.start_npz(data)
	



if __name__ == '__main__':
	app    = QtWidgets.QApplication(sys.argv)
	widget = MainPanel()
	widget.show()
	sys.exit(app.exec_())
