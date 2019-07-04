#!/usr/bin/env python

import sys,os
from PyQt5 import QtWidgets, QtCore, QtGui, uic
from dataio import DataLandmarks,DataManual
from panel_main import MainPanel
from panel_landmarks import LandmarksPanel
from panel_manual import ManualPanel
from widgets import MenuBar


class MainWindow(QtWidgets.QMainWindow):
	def __init__(self, argv):
		super().__init__()
		fnameUI  = os.path.join( os.path.dirname(__file__), 'main.ui' )
		uic.loadUi(fnameUI, self)
		
		
		# self.centralWidget = QtWidgets.QWidget(self)
		# self.setCentralWidget(self.centralWidget)
		
		
		
		
		self.label0.setVisible(False)
		self.label1.setVisible(False)
		self.label2.setVisible(False)
		
		self.panel_main      = MainPanel(self)
		self.panel_landmarks = LandmarksPanel(self)
		self.panel_manual    = ManualPanel(self)
		self.setMenuBar( MenuBar(self) )
		# self.panel_main      = MainPanel(self)
		# self.panel_landmarks = LandmarksPanel(self)
		# self.panel_manual    = ManualPanel(self)
		# self.setMenuBar( MenuBar(self) )
		self._set_panel(0)
		
		self.hlayout0.addWidget( self.panel_main )
		self.hlayout1.addWidget( self.panel_landmarks )
		self.hlayout2.addWidget( self.panel_manual )
		
		self.hlayout0.layout()
		
		
		# self.setFixedSize(1300, 850)
		# self.setFixedSize(1300, 400)
		
		self._parse_commandline_inputs(argv)
		
		
		
		
	
	
	def _parse_commandline_inputs(self, argv):
		narg     = len(argv)
		fnameCSV = argv[1] if narg>1 else None
		mode     = argv[2] if narg>2 else None
		fnameNPZ = argv[3] if narg>3 else None
		
		#default output filename:
		if fnameNPZ is None:
			if fnameCSV is None:
				fnameNPZ    = os.path.join( os.getcwd(), '_mwarp1d.npz' )
			else:
				fnameNPZ    = os.path.join( os.path.dirname(fnameCSV), '_mwarp1d.npz' )
			print('\n\n\nWelcome to mwarp1d!\n\nSession data will be saved to %s.\n\nTo save to a different location, change the "Results file" option.\n\n\n' %fnameNPZ)


		if mode is not None:
			if mode not in ['landmarks', 'manual']:
				raise ValueError('Unknown mode: %s ("mode" must be either "landmarks" or "manual")' %mode)
			if mode == 'landmarks':
				data = DataLandmarks()
				self.panel_landmarks.set_data(data)
				self._set_panel(1)
			elif mode == 'manual':
				data = DataManual()
				self.panel_manual.set_data(data)
				self._set_panel(2)
			data.set_input_filename( fnameCSV )
			data.set_output_filename( fnameNPZ )
			data.save()
				

		

	def _set_panel(self, ind):
		self.stackedWidget.setCurrentIndex(ind)
		if ind==0:
			self.menuBar().set_main_panel_menu()
		elif ind==1:
			self.menuBar().set_landmarks_panel_menu()
		elif ind==2:
			self.menuBar().set_manual_panel_menu()
		

	def get_results_filename(self, fname0, fname1=None):
		if fname1 is None:
			dir0 = os.path.dirname(fname0)
			fname1 = os.path.join(dir0, 'mwarp1d.npz')
		return fname1
		
	
	def start_landmark_mode(self, template, sources, fname0, fname1=None):
		fname1 = self.get_results_filename(fname0, fname1)
		data   = DataLandmarks()
		data.set_input_filename( fname0, read=False )
		data.set_output_filename( fname1 )
		data.set_template(template)
		data.set_sources(sources, init_warped=True)
		data.save()
		self.panel_landmarks.set_data(data)
		self._set_panel(1)
		



	def start_manual_mode(self, template, sources, fname0, fname1=None):
		fname1 = self.get_results_filename(fname0, fname1)
		data   = DataManual()
		data.set_input_filename( fname0, read=False )
		data.set_output_filename( fname1 )
		data.set_template(template)
		data.set_sources(sources, init_warped=True)
		data.save()
		self.panel_manual.set_data(data)
		self._set_panel(2)
		
		
	def start_npz(self, data):
		if data.mode == 'landmarks':
			self.panel_landmarks.set_data(data, prewarped=True)
			self._set_panel(1)
		else:
			self.panel_manual.set_data(data, prewarped=True)
			self._set_panel(2)
		
		

class MainApplication(QtWidgets.QApplication):
	def __init__(self, *args):
		self.setApplicationName("Appname")
		super().__init__(*args)
		# style = QtWidgets.QStyleFactory.create('Fusion')
		# self.setStyle(style)



if __name__ == '__main__':
	app    = MainApplication(sys.argv)
	app.setApplicationName("mwarp1d")
	window = MainWindow( sys.argv )
	window.move(0, 0)
	window.show()
	sys.exit(app.exec_())
	
	
	
	
