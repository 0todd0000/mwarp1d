
from PyQt5 import QtWidgets, QtCore, QtGui

from . import FileSaveDialog


class _Menu(QtWidgets.QMenu):
	title            = 'Menu Name'
	
	def __init__(self, mainapp, panel=None):
		super().__init__(mainapp)
		self.mainapp = mainapp
		self.panel   = panel
		self.setTitle( self.title )

	def _grab(self, obj):
		dialog = FileSaveDialog('jpg')
		if dialog.exec_() == QtWidgets.QDialog.Accepted:
			fname = dialog.selectedFiles()[0]
			p     = obj.grab()
			p.save(fname, 'jpg')

	def on_export_csv_warped(self):
		dialog = FileSaveDialog('csv')
		if dialog.exec_() == QtWidgets.QDialog.Accepted:
			fname  = dialog.selectedFiles()[0]
			self.panel.data.write_sources_warped_csv(fname)

	def on_export_mat(self):
		dialog = FileSaveDialog('mat')
		if dialog.exec_() == QtWidgets.QDialog.Accepted:
			fname = dialog.selectedFiles()[0]
			self.panel.data.write_mat(fname)

	def on_screenshot_window(self):
		self._grab( self.mainapp )


class MainFileMenu(_Menu):
	title            = 'Load'
	
	def __init__(self, mainapp):
		super().__init__(mainapp)
		action0      = QtWidgets.QAction('Load 1D data', self)
		action1      = QtWidgets.QAction('Load mwarp1d file', self)
		action0.triggered.connect( self.on_load_data)
		action1.triggered.connect( self.on_load_mwarp1d)
		self.addAction(action0)
		self.addAction(action1)
	
	def on_load_data(self):
		fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', None, "CSV files (*.csv)")[0]
		if fname != '':
			self.mainapp.panel_main.on_drop([fname])

	def on_load_mwarp1d(self):
		fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', None, "NPZ files (*.npz)")[0]
		if fname != '':
			self.mainapp.panel_main.on_drop([fname])




class LandmarksExportMenu(_Menu):
	title            = 'Export'
	
	def __init__(self, mainapp):
		super().__init__(mainapp, mainapp.panel_landmarks)
		### CSV menu:
		menu_csv    = QtWidgets.QMenu('CSV', self)
		export0     = QtWidgets.QAction('Warped 1D data', self)
		export1     = QtWidgets.QAction('Landmarks', self)
		export2     = QtWidgets.QAction('MAT', self)
		menu_csv.addAction(export0)
		menu_csv.addAction(export1)
		### add actions:
		self.addMenu(menu_csv)
		self.addAction(export2)
		### callbacks:
		export0.triggered.connect( self.on_export_csv_warped )
		export1.triggered.connect( self.on_export_csv_landmarks )
		export2.triggered.connect( self.on_export_mat )
		
	def on_export_csv_landmarks(self):
		dialog = FileSaveDialog('csv')
		if dialog.exec_() == QtWidgets.QDialog.Accepted:
			fname  = dialog.selectedFiles()[0]
			self.mainapp.panel_landmarks.data.write_landmarks_csv(fname)
	





class LandmarksScreenshotMenu(_Menu):
	
	title            = 'Screenshot'
	
	def __init__(self, mainapp):
		super().__init__(mainapp)
		screenshot0 = QtWidgets.QAction('Window', self)
		screenshot1 = QtWidgets.QAction('Figure: Landmarks', self)
		screenshot2 = QtWidgets.QAction('Figure: Warped', self)
		### screenshot actions:
		self.addAction(screenshot0)
		self.addAction(screenshot1)
		self.addAction(screenshot2)
		### screenshot callbacks:
		screenshot0.triggered.connect( self.on_screenshot_window )
		screenshot1.triggered.connect( self.on_screenshot_figure_landmarks )
		screenshot2.triggered.connect( self.on_screenshot_figure_warped )
		
		
	def on_screenshot_figure_landmarks(self):
		self._grab( self.mainapp.panel_landmarks.figure0 )

	def on_screenshot_figure_warped(self):
		self._grab( self.mainapp.panel_landmarks.figure1 )
	




class ManualExportMenu(_Menu):
	title            = 'Export'
	
	def __init__(self, mainapp):
		super().__init__(mainapp, mainapp.panel_manual)
		### CSV menu:
		menu_csv    = QtWidgets.QMenu('CSV', self)
		export0     = QtWidgets.QAction('Warped 1D data', self)
		export2     = QtWidgets.QAction('MAT', self)
		menu_csv.addAction(export0)
		### add actions:
		self.addMenu(menu_csv)
		self.addAction(export2)
		### callbacks:
		export0.triggered.connect( self.on_export_csv_warped )
		export2.triggered.connect( self.on_export_mat )


class ManualScreenshotMenu(_Menu):
	
	title            = 'Screenshot'
	
	def __init__(self, mainapp):
		super().__init__(mainapp)
		screenshot0 = QtWidgets.QAction('Window', self)
		screenshot1 = QtWidgets.QAction('Figure', self)
		### screenshot actions:
		self.addAction(screenshot0)
		self.addAction(screenshot1)
		### screenshot callbacks:
		screenshot0.triggered.connect( self.on_screenshot_window )
		screenshot1.triggered.connect( self.on_screenshot_figure )

	def on_screenshot_figure(self):
		self._grab( self.mainapp.panel_manual.figure )
	



class MenuBar(QtWidgets.QMenuBar):
	def __init__(self, parent):
		super().__init__(parent)
		self.mainapp    = parent

	def on_quit(self):
		print('mwarp1d:  Bye!')
		QtWidgets.qApp.quit()

	def set_main_panel_menu(self):
		self.clear()
		self.addMenu( MainFileMenu(self.mainapp) )

	def set_landmarks_panel_menu(self):
		self.clear()
		self.addMenu( LandmarksExportMenu(self.mainapp) )
		self.addMenu( LandmarksScreenshotMenu(self.mainapp) )
		
	def set_manual_panel_menu(self):
		self.clear()
		self.addMenu( ManualExportMenu(self.mainapp) )
		self.addMenu( ManualScreenshotMenu(self.mainapp) )


