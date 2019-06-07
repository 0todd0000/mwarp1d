#!/usr/bin/env python

import sys,os
from PyQt5 import QtWidgets, QtCore, QtGui, uic
from . dataio import DataLandmarks,DataManual
from . panel_main import MainPanel
from . panel_landmarks import LandmarksPanel
from . panel_manual import ManualPanel
from . widgets import MenuBar


class MainWindow(QtWidgets.QMainWindow):
	def __init__(self, argv):
		super().__init__()
		fnameUI  = os.path.join( os.path.dirname(__file__), 'main.ui' )
		uic.loadUi(fnameUI, self)
		
		self.label0.setVisible(False)
		self.label1.setVisible(False)
		self.label2.setVisible(False)
		
		self.panel_main      = MainPanel(self)
		self.panel_landmarks = LandmarksPanel(self)
		self.panel_manual    = ManualPanel(self)
		self.setMenuBar( MenuBar(self) )
		self._set_panel(0)
		
		self.hlayout0.addWidget( self.panel_main )
		self.hlayout1.addWidget( self.panel_landmarks )
		self.hlayout2.addWidget( self.panel_manual )
		
		self._parse_commandline_inputs(argv)
		
	
	
	def _parse_commandline_inputs(self, argv):
		narg   = len(argv)
		if narg > 1:
			mode   = argv[1]
			fname0 = argv[2]
			fname1 = argv[3] if (len(argv) > 3) else None
		
			if mode == 'landmarks':
				data = DataLandmarks()
			elif mode == 'manual':
				data = DataManual()
			else:
				raise ValueError('Unknown mode: %s ("mode" must be either "landmarks" or "manual")' %mode)

			data.set_input_filename( fname0 )
			data.set_output_filename( fname1 )
			data.save()
		
			if mode == 'landmarks':
				self.panel_landmarks.set_data(data)
				self._set_panel(1)
			elif mode == 'manual':
				self.panel_manual.set_data(data)
				self._set_panel(2)
			
		

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



if __name__ == '__main__':
	app    = MainApplication(sys.argv)
	app.setApplicationName("mwarp1d")
	window = MainWindow( sys.argv )
	window.move(0, 0)
	window.show()
	sys.exit(app.exec_())
