#!/usr/bin/env python

import sys,os
from PyQt5 import QtWidgets, QtCore, QtGui, uic
import numpy as np
from widgets import MessageBox,SimpleDialog
import mwarp1d







class LandmarksPanel(QtWidgets.QWidget):
	
	template_locked      = QtCore.pyqtSignal(bool)
	
	
	def __init__(self, parent=None):
		super().__init__(parent=parent)
		fnameUI  = os.path.join( os.path.dirname(__file__), 'panel_landmarks.ui' )
		uic.loadUi(fnameUI, self)
		self.data                = None
		self.is_template_locked  = False
		self.is_template_visible = True
		self.is_unselected_visible = True
		self.mainapp   = parent
		self.template  = None
		self.sources   = None

		
		
		self.button_lock_template.setFocus(True)
		
		### connect callbacks (panel controls):
		self.button_next_curve.clicked.connect( self.on_next_curve )
		self.button_previous_curve.clicked.connect( self.on_previous_curve )
		self.button_lock_template.clicked.connect( self.on_button_lock_template )
		
		### connect callbacks (custom controls):
		self.table0.template_table_row_selected.connect( self.on_template_table_row_selected )
		self.table0.colname_changed.connect( self.on_colname_changed )
		self.table1.rows_selected.connect( self.on_source_table_row_selected )
		self.table1.rowflags_changed.connect( self.on_source_rowflags_changed )		
		
		self.box_table1.setEnabled(False)
		self.button_next_curve.setEnabled(False)
		self.button_previous_curve.setEnabled(False)
		self.label_current_curve.setEnabled(False)
		
		

		shortcut_left  = QtWidgets.QShortcut( QtGui.QKeySequence( QtCore.Qt.Key_Left ), self )
		shortcut_right = QtWidgets.QShortcut( QtGui.QKeySequence( QtCore.Qt.Key_Right ), self )
		shortcut_A     = QtWidgets.QShortcut( QtGui.QKeySequence( QtCore.Qt.Key_A ), self )
		shortcut_L     = QtWidgets.QShortcut( QtGui.QKeySequence( QtCore.Qt.Key_L ), self )
		shortcut_S     = QtWidgets.QShortcut( QtGui.QKeySequence( QtCore.Qt.Key_S ), self )
		shortcut_T     = QtWidgets.QShortcut( QtGui.QKeySequence( QtCore.Qt.Key_T ), self )
		shortcut_Y     = QtWidgets.QShortcut( QtGui.QKeySequence( QtCore.Qt.Key_Y ), self )
		
		shortcut_left.activated.connect( self.on_left_arrow )
		shortcut_right.activated.connect( self.on_right_arrow )
		shortcut_A.activated.connect( self.on_add_landmark_keyboard )
		shortcut_L.activated.connect( self.toggle_template_locked )
		shortcut_S.activated.connect( self.toggle_unselected_visible )
		shortcut_T.activated.connect( self.toggle_template_visible )
		shortcut_Y.activated.connect( self.toggle_legend_visible )
		
		

		
	def _initiate_using_data(self, data):
		y0     = data.ydata_template
		y      = data.ydata_sources
	
		J,Q    = y.shape
		a0     = np.asarray([0.25*Q, 0.50*Q, 0.75*Q], dtype=int).tolist()
		A      = np.vstack([a0]*J)
		
		
		data.landmarks_template  = np.array(a0)
		data.landmarks_sources   = A
		data.landmark_labels     = ['L0', 'L1', 'L2']
		data.save()
		
		
		
		
		self.figure0._init(y0, y, a0, A)
		self.figure1._init(y0, y)

		self.figure0.curve_left_click_selected.connect(self.on_curve_left_click_selected)
		self.figure0.curve_arrow_selected.connect( self.on_curve_arrow_selected )
		self.figure0.dragging_stopped.connect( self.on_landmark_dragging_stopped )
		self.figure0.template_point_dragged.connect( self.on_template_point_dragged )
		self.figure0.source_point_dragged.connect( self.on_source_point_dragged )
		self.figure0.template_landmark_added.connect( self.on_template_landmark_added )
		self.figure0.landmark_deleted.connect( self.on_landmark_deleted )
		

		self.figure0.maxlandmarksreached.connect( self.on_maxlandmarks_reached )
		self.figure0.tsplot.template.landmarks.point_deleted.connect( self.on_template_landmark_deleted )
		self.figure0.tsplot.template.landmarks.point_delete_failed.connect( self.on_template_landmark_delete_failed )


		template_landmarks = self.figure0.get_template_landmarks_object()
		source_landmarks   = self.figure0.get_source_landmarks_objects()


		### initialize tables:
		self.table0._init( [template_landmarks] )
		self.table1._init( source_landmarks )

		self.table0.verticalHeader().sectionPressed.emit(0)
		self.table1.set_null_values()

		
		self.figure0.set_sources_visible(False)
		self.figure1.set_visible(False)
		




	def _initiate_using_prewarped_data(self, data):

		
		y0     = data.ydata_template
		y      = data.ydata_sources
		yw     = data.ydata_sources_warped
		a0     = data.landmarks_template
		A      = data.landmarks_sources
	
		
		
		self.figure0._init(y0, y, a0, A)
		self.figure1._init(y0, y)
		for hh,yy in zip(self.figure1.h, yw):
			hh.set_ydata(yy)
		
		
		### initialize tables:
		template_landmarks = self.figure0.get_template_landmarks_object()
		source_landmarks   = self.figure0.get_source_landmarks_objects()
		
		template_landmarks.set_all_xdata(a0)
		for a,source in zip(A,source_landmarks):
			# source.set_all_xdata(a)
			source.h.set_xdata(a)
		
		self.table0._init( [template_landmarks], data.landmark_labels )
		self.table1._init( source_landmarks, data.landmark_labels )
		
	
		
		self.button_lock_template.setChecked( True )
		self.on_button_lock_template(True, overwrite_source_landmarks=False)




		self.figure0.curve_left_click_selected.connect(self.on_curve_left_click_selected)
		self.figure0.curve_arrow_selected.connect( self.on_curve_arrow_selected )
		self.figure0.dragging_stopped.connect( self.on_landmark_dragging_stopped )
		self.figure0.template_point_dragged.connect( self.on_template_point_dragged )
		self.figure0.source_point_dragged.connect( self.on_source_point_dragged )
		self.figure0.template_landmark_added.connect( self.on_template_landmark_added )
		self.figure0.landmark_deleted.connect( self.on_landmark_deleted )

		self.figure0.maxlandmarksreached.connect( self.on_maxlandmarks_reached )
		self.figure0.tsplot.template.landmarks.point_deleted.connect( self.on_template_landmark_deleted )
		self.figure0.tsplot.template.landmarks.point_delete_failed.connect( self.on_template_landmark_delete_failed )

		self.table0.verticalHeader().sectionPressed.emit(0)
		self.table1.set_null_values(False)
		self.figure1.set_visible(True)
		


	def _save_landmark_tables(self, commit=True):
		names  = self.table0.get_landmark_names()
		a0     = self.table0.get_table_as_array()
		A      = self.table1.get_table_as_array()
		self.data.set_landmark_labels(names)
		self.data.set_template_landmarks(a0)
		self.data.set_source_landmarks(A)
		if commit:
			self.data.save()

	def _save_warped_sources(self):
		self.data.set_sources_warped( self.figure1.get_warped_sources_as_array() )
		self.data.save()	

	
	def get_landmark_names(self):
		return self.table0.get_landmark_names()
	

	# def toggle_lock_template(self):
	# 	button = self.button_lock_template
	# 	locked = button.isChecked()
	# 	button.setChecked( not locked )
	# 	self.on_button_lock_template( not locked )
	
	
	
	def on_add_landmark_keyboard(self):
		self.figure0.tsplot.add_landmark()
	
	
	def on_button_lock_template(self, locked, overwrite_source_landmarks=True):
		self.is_template_locked = locked
		if locked:
			self.button_lock_template.setText('Unlock Template')
			self.box_table1.setEnabled(True)
			self.button_next_curve.setEnabled(True)
			self.button_previous_curve.setEnabled(True)
			self.label_current_curve.setEnabled(True)

			if overwrite_source_landmarks:
				self.figure0.reset_source_landmarks()
			self.table1.set_null_values(False)
			self.figure0.set_template_locked(True)

			self.figure1.set_visible(True)
			
		else:
			dialog   = SimpleDialog('All source landmarks will be reset.')
			accepted = dialog.exec()
			if accepted:
				self.button_lock_template.setText('Lock Template')
				
				self.box_table1.setEnabled(False)
				self.button_next_curve.setEnabled(False)
				self.button_previous_curve.setEnabled(False)
				self.label_current_curve.setEnabled(False)
				
				self.table1.set_null_values(True)
				self.figure0.reset_source_landmarks()
				self.figure0.set_template_visible(True)
				self.figure0.set_template_active()
				self.figure0.set_template_locked(False)
				
				self.figure1.set_visible(False)
		self.button_lock_template.repaint()

		
		


	def on_checkbox_template(self, checked):
		self.set_template_visible(checked)
		

	def on_colname_changed(self, col, s):
		self.table1.set_collabel(col, s)
		
		names = self.get_landmark_names()
		self.data.set_landmark_labels(names)
		self.data.save()
		
		
		
		
		
	
	def on_curve_arrow_selected(self, ind):
		if ind==0:
			self.table0.verticalHeader().sectionPressed.emit(0)
			self.table1.verticalHeader().clearSelection()
			self.figure1.clear_source_selection()
		else:
			self.table0.verticalHeader().clearSelection()
			self.table1.verticalHeader().sectionPressed.emit(ind-1)
			self.figure1.set_source_selected(ind-1)
		self.label_current_curve.setText( str(ind) )
		self.repaint()
		

	
	def on_curve_left_click_selected(self, ind):
		self.label_current_curve.setText( str(ind) )
		if ind==0:
			self.table0.verticalHeader().sectionPressed.emit(0)
			self.table1.verticalHeader().clearSelection()
			self.figure1.clear_source_selection()
		else:
			self.table0.verticalHeader().clearSelection()
			self.table1.verticalHeader().sectionPressed.emit(ind-1)
			self.figure1.set_source_selected(ind-1)
	
		
	def on_landmark_dragging_stopped(self):
		self._save_landmark_tables(commit=False)
		self._save_warped_sources()
		
		
	def on_landmark_add_attempt_but_disabled(self):
		MessageBox('Unlock the Template  to add / delete points')

	def on_landmark_delete_attempt_but_disabled(self):
		MessageBox('Unlock the Template  to add / delete points')
	
	
	
	
	def on_landmark_changed(self, ind, val):
		self.table0.set_cell_value(0, ind, val)
		

		
	
	def on_landmark_deleted(self, ind):
		self._save_landmark_tables()
		
	def on_left_arrow(self):
		self.on_previous_curve()

	def on_maxlandmarks_reached(self, n):
		MessageBox('The maximum number of landmarks is %d' %n)


	def on_next_curve(self):
		if self.is_template_locked:
			self.figure0.set_next_selected()
			self.update_warped_plot_source_visibility()
		
		
	def on_previous_curve(self):
		if self.is_template_locked:
			self.figure0.set_previous_selected()
			self.update_warped_plot_source_visibility()


	def on_right_arrow(self):
		self.on_next_curve()
	
	
	
	def on_source_point_dragged(self, row, ind, x, y):
		self.table1.set_cell_value(row, ind, x)
		p    = self.figure0.tsplot
		y    = p._sources0[row]
		x0   = p.template.landmarks.h.get_xdata()
		x    = p.sources[row].landmarks.h.get_xdata()
		x0   = [0] + x0.tolist() + [p.Q-1]
		x    = [0] + x.tolist() + [p.Q-1]
		yw   = mwarp1d.warp1d_landmarks(y, x0, x)
		self.figure1.h[row].set_ydata( yw )
		self.figure1.ax.figure.canvas.draw()
		
	
	def on_source_rowflags_changed(self):
		print('on_source_rowflags_changed')
		self.figure0.update_flagged_source_colors()

	
	def on_source_table_row_selected(self, rowlist):
		self.table0.verticalHeader().clearSelection()
		if len(rowlist)==1:
			self.figure0.select_source_by_table_header_click( rowlist[0] )
			self.label_current_curve.setText( str(rowlist[0]+1) )
			self.figure1.set_source_selected(rowlist[0])
		else:
			pass


	

	def on_template_landmark_added(self, ind, value):
		self.table0.add_column(ind)
		x = self.figure0.tsplot.template.landmarks.get_xdata()
		for source in self.figure0.tsplot.sources:
			source.landmarks.add_point(value)
		self.table1.add_column(ind)
		self._save_landmark_tables()
		

	def on_template_landmark_delete_failed(self):
		MessageBox('There must be at least one landmark.')

	def on_template_landmark_deleted(self, ind):
		self.table0.delete_column(ind)
		x = self.figure0.tsplot.template.landmarks.get_xdata()
		for source in self.figure0.tsplot.sources:
			source.landmarks.delete_point(ind)
		self.table1.delete_column(ind)
		self._save_landmark_tables()
		

	def on_template_point_dragged(self, ind, x, y):
		self.table0.set_cell_value(0, ind, x)
	
	def on_template_table_row_selected(self):
		self.figure0.set_template_selected()
		self.table1.verticalHeader().clearSelection()
		# self.figure0.select_template()
		self.label_current_curve.setText( '0' )
	

	
	def rename_landmark(self, col):
		s0  = self.table0.horizontalHeaderItem(col).text()
		### open dialog:
		dlg = QtWidgets.QInputDialog(self)
		dlg.setInputMode( QtWidgets.QInputDialog.TextInput )
		dlg.setLabelText('Edit Landmark Name')
		dlg.setTextValue(s0)
		dlg.move( QtGui.QCursor.pos() )
		ok = dlg.exec_()
		### update labels:
		if ok:
			s = dlg.textValue()
			self.table0.horizontalHeaderItem(col).setText(s)
			self.table1.horizontalHeaderItem(col).setText(s)



	def set_data(self, data, prewarped=False):
		self.data = data
		if prewarped:
			self._initiate_using_prewarped_data(data)
		else:
			self._initiate_using_data(data)
	
	
	def set_template_visible(self, visible):
		self.figure0.set_template_visible(visible)
	
	
	
	def toggle_legend_visible(self):
		self.figure0.tsplot.toggle_legend_visible()
	
	def toggle_template_locked(self):
		self.is_template_locked = not self.is_template_locked
		self.button_lock_template.setChecked( self.is_template_locked )
		self.on_button_lock_template( self.is_template_locked )
		self.template_locked.emit( self.is_template_locked )
	
	def toggle_template_visible(self):
		if self.is_template_locked:
			self.is_template_visible = not self.is_template_visible
			self.figure0.tsplot.template.set_visible( self.is_template_visible )
			self.figure0.ax.figure.canvas.draw()
			self.figure1.set_template_visible(self.is_template_visible)
			self.figure1.ax.figure.canvas.draw()
	
	def toggle_unselected_visible(self):
		if self.is_template_locked:
			self.figure0.toggle_unselected_visible()
			self.is_unselected_visible = not self.is_unselected_visible
			self.update_warped_plot_source_visibility()
	
	def update_counts(self):
		self.label_nsources.setText( str(self.table1.nrow) )
		self.label_nlandmarks.setText( str(self.table0.ncol) )
		
	

		
	
	def update_warped_plot_source_visibility(self):
		if self.is_unselected_visible:
			self.figure1.set_sources_visible(True)
		else:
			visible = [source.line.isactive for source in self.figure0.tsplot.sources]
			self.figure1.set_sources_visible_bool_list(visible)
		self.figure1.ax.figure.canvas.draw()





if __name__ == '__main__':
	app    = QtWidgets.QApplication(sys.argv)
	widget = LandmarksPanel()
	widget.move(0, 0)
	widget.show()
	sys.exit(app.exec_())
