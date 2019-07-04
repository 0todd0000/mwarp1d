
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
		dialog = FileSaveDialog('jpg', self.mainapp.dir0)
		if dialog.exec_() == QtWidgets.QDialog.Accepted:
			fname = dialog.selectedFiles()[0]
			p     = obj.grab()
			p.save(fname, 'jpg')

	def on_export_csv_warped(self):
		dialog = FileSaveDialog('csv', self.mainapp.dir0)
		if dialog.exec_() == QtWidgets.QDialog.Accepted:
			fname  = dialog.selectedFiles()[0]
			self.panel.data.write_sources_warped_csv(fname)

	def on_export_mat(self):
		dialog = FileSaveDialog('mat', self.mainapp.dir0)
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
		dialog = FileSaveDialog('csv', self.mainapp.dir0)
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




class LandmarksQuickKeyMenu(_Menu):
	
	title            = 'Quick keys'
	
	def __init__(self, mainapp):
		super().__init__(mainapp)
		self.panel     = mainapp.panel_landmarks
		self._actions  = []
		a0 = QtWidgets.QAction('S :   Sources:  toggle visible', self)
		a1 = QtWidgets.QAction('T :   Template: toggle visible', self)
		a2 = QtWidgets.QAction('Y :   Legend:   toggle visible', self)
		a3 = QtWidgets.QAction('Left arrow :   previous curve', self)
		a4 = QtWidgets.QAction('Right arrow :   next curve', self)
		a5 = QtWidgets.QAction('A :   Add landmark', self)
		a6 = QtWidgets.QAction('L :   Lock template', self)
		### actions:
		self.addAction(a0)
		self.addAction(a1)
		self.addAction(a2)
		self.addSection('Selection')
		self.addAction(a3)
		self.addAction(a4)
		self.addSection('Functions')
		self.addAction(a5)
		self.addAction(a6)
		### callbacks:
		a0.triggered.connect( self.on_toggle_source_visibility )
		a1.triggered.connect( self.on_toggle_template_visibility )
		a2.triggered.connect( self.on_toggle_legend_visibility )
		a3.triggered.connect( self.on_select_previous )
		a4.triggered.connect( self.on_select_next )
		a5.triggered.connect( self.on_add_landmark )
		a6.triggered.connect( self.on_toggle_template_lock )
		### enabled states:
		[a.setEnabled(False) for a in [a0,a1,a3,a4]]

	def addAction(self, action):
		super().addAction(action)
		self._actions.append(action)
	
	
	def on_add_landmark(self):
		self.panel.on_add_landmark_keyboard()
	
	def on_select_next(self):
		self.panel.on_next_curve()

	def on_select_previous(self):
		self.panel.on_previous_curve()

	def on_toggle_legend_visibility(self):
		self.panel.toggle_legend_visible()
	
	def on_toggle_source_visibility(self):
		self.panel.toggle_unselected_visible()

	def on_toggle_template_lock(self):
		self.panel.toggle_template_locked()
		
	def on_toggle_template_visibility(self):
		self.panel.toggle_template_visible()
		
		
	def update_template_locked(self, locked):
		self._actions[0].setEnabled(locked)
		self._actions[1].setEnabled(locked)
		self._actions[3].setEnabled(locked)
		self._actions[4].setEnabled(locked)
		self._actions[5].setEnabled(not locked)
		if locked:
			self._actions[6].setText('L :   Unlock template')
		else:
			self._actions[6].setText('L :   Lock template')





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
	




class ManualQuickKeyMenu(_Menu):
	
	title            = 'Quick keys'
	
	def __init__(self, mainapp):
		super().__init__(mainapp)
		self._actions  = []
		self.panel     = mainapp.panel_manual
		a0 = QtWidgets.QAction('S :   Sources:  toggle visible', self)
		a1 = QtWidgets.QAction('T :   Template: toggle visible', self)
		a2 = QtWidgets.QAction('Y :   Legend:   toggle visible', self)
		a3 = QtWidgets.QAction('Left arrow :   previous curve', self)
		a4 = QtWidgets.QAction('Right arrow :   next curve', self)
		a5 = QtWidgets.QAction('W :   initialize Warp', self)
		a6 = QtWidgets.QAction('RETURN :   apply warp', self)
		a7 = QtWidgets.QAction('ESC :   cancel warp', self)
		a8 = QtWidgets.QAction('O :   Original source: toggle visible', self)
		a9 = QtWidgets.QAction('R :   Reset source', self)
		### actions:
		self.addAction(a0)
		self.addAction(a1)
		self.addAction(a2)
		self.addSection('Arrows')
		self.addAction(a3)
		self.addAction(a4)
		self.addSection('Warps')
		self.addAction(a5)
		self.addAction(a6)
		self.addAction(a7)
		self.addSection('Visibility')
		self.addAction(a8)
		self.addAction(a9)
		### callbacks:
		a0.triggered.connect( self.panel.on_key_s )
		a1.triggered.connect( self.panel.on_key_t )
		a2.triggered.connect( self.panel.on_key_y )
		a3.triggered.connect( self.panel.on_previous_curve )
		a4.triggered.connect( self.panel.on_next_curve )
		a5.triggered.connect( self.panel.on_key_w )
		a6.triggered.connect( self.panel.on_key_return )
		a7.triggered.connect( self.panel.on_key_escape )
		a8.triggered.connect( self.panel.on_key_o )
		a9.triggered.connect( self.panel.on_key_r )
		### enable:
		for a in [a5,a6,a7,a8,a9]:
			a.setEnabled(False)


	def _enable_arrows(self, enable):
		self._actions[3].setEnabled( enable )
		self._actions[4].setEnabled( enable )

	def _enable_warp_controls(self, enable):
		self._actions[6].setEnabled( enable )
		self._actions[7].setEnabled( enable )
		
	
	def addAction(self, action):
		super().addAction(action)
		self._actions.append(action)
	
	
	def update_manual_curve_selected(self, ind):
		enable = ind!=0
		self._actions[5].setEnabled( enable )
		self._actions[8].setEnabled( enable )
		self._actions[9].setEnabled( enable )

	def update_warp_applied(self):
		self._enable_arrows(True)
		self._enable_warp_controls(False)
	def update_warp_cancelled(self):
		self._enable_arrows(True)
		self._enable_warp_controls(False)
	def update_warp_initiated(self):
		self._enable_arrows(False)
		self._enable_warp_controls(True)



class MenuBar(QtWidgets.QMenuBar):
	def __init__(self, parent):
		super().__init__(parent)
		self.mainapp    = parent
		self.menus      = []

	def addMenu(self, menu):
		super().addMenu(menu)
		self.menus.append(menu)
	
	def clear(self):
		super().clear()
		self.menus      = []
	
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
		self.addMenu( LandmarksQuickKeyMenu(self.mainapp) )
		
	def set_manual_panel_menu(self):
		self.clear()
		self.addMenu( ManualExportMenu(self.mainapp) )
		self.addMenu( ManualScreenshotMenu(self.mainapp) )
		self.addMenu( ManualQuickKeyMenu(self.mainapp) )
		
		
		
	def update_template_locked(self, locked):
		self.menus[2].update_template_locked(locked)

	def update_manual_curve_selected(self, ind):
		self.menus[2].update_manual_curve_selected(ind)
	
	def update_warp_applied(self):
		self.menus[2].update_warp_applied()
	def update_warp_cancelled(self):
		self.menus[2].update_warp_cancelled()
	def update_warp_initiated(self):
		self.menus[2].update_warp_initiated()

