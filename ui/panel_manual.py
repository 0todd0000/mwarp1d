
import sys,os
from math import floor
from PyQt5 import QtWidgets, QtCore, QtGui, uic
import numpy as np
from widgets import MessageBox,SimpleDialog
import mwarp1d





class ManualPanel(QtWidgets.QWidget):
	def __init__(self, parent=None):
		super().__init__(parent=parent)
		fnameUI  = os.path.join( os.path.dirname(__file__), 'panel_manual.ui' )
		uic.loadUi(fnameUI, self)
		
		self.data                    = None
		self.iscurveselectionenabled = True
		
		self.warp    = mwarp1d.ManualWarp1D(1001)
		self.warp_controls.set_warp(self.warp)
		self.warp_controls.button_initiate.setEnabled(False)

		self.button_next_curve.clicked.connect( self.on_next_curve )
		self.button_previous_curve.clicked.connect( self.on_previous_curve )
		self.spin_current_curve.valueChanged.connect( self.on_spin_current_curve )
		self.spin_current_curve.setMinimum(0)
		self.spin_current_curve.setMaximum(0)
		
		self.warp_controls.applied.connect( self.on_button_warp_applied )
		self.warp_controls.cancelled.connect( self.on_button_warp_cancelled )
		self.warp_controls.initiated.connect( self.on_button_warp_initiated )

		shortcut_left   = QtWidgets.QShortcut( QtGui.QKeySequence( QtCore.Qt.Key_Left ), self )
		shortcut_right  = QtWidgets.QShortcut( QtGui.QKeySequence( QtCore.Qt.Key_Right ), self )
		shortcut_Escape = QtWidgets.QShortcut( QtGui.QKeySequence( QtCore.Qt.Key_Escape ), self )
		shortcut_Return = QtWidgets.QShortcut( QtGui.QKeySequence( QtCore.Qt.Key_Return ), self )
		shortcut_O      = QtWidgets.QShortcut( QtGui.QKeySequence( QtCore.Qt.Key_O ), self )
		shortcut_R      = QtWidgets.QShortcut( QtGui.QKeySequence( QtCore.Qt.Key_R ), self )
		shortcut_S      = QtWidgets.QShortcut( QtGui.QKeySequence( QtCore.Qt.Key_S ), self )
		shortcut_T      = QtWidgets.QShortcut( QtGui.QKeySequence( QtCore.Qt.Key_T ), self )
		shortcut_W      = QtWidgets.QShortcut( QtGui.QKeySequence( QtCore.Qt.Key_W ), self )
		
		shortcut_left.activated.connect( self.on_previous_curve )
		shortcut_right.activated.connect( self.on_next_curve )
		shortcut_Escape.activated.connect( self.on_key_escape )
		shortcut_Return.activated.connect( self.on_key_return )
		shortcut_O.activated.connect( self.on_key_o )
		shortcut_R.activated.connect( self.on_key_r )
		shortcut_S.activated.connect( self.on_key_s )
		shortcut_T.activated.connect( self.on_key_t )
		shortcut_W.activated.connect( self.on_key_w )

	

	def _initiate_using_data(self, data):
		y0     = data.ydata_template
		y      = data.ydata_sources
		
		J,Q    = y.shape
		self.label_nsources.setText( str(J) )
		self.spin_current_curve.setMaximum( J )

		#initialize figure:
		self.warp.set_domain_size(Q)
		self.figure._init(y0, y)
		self.figure.tsplot.set_warp(self.warp)

		#callbacks:
		self.figure.tsplot.axes_entered.connect( self.on_axes_entered )
		self.figure.tsplot.curve_activated.connect( self.on_signal_curve_activated )
		self.figure.tsplot.warp_click_applied.connect( self.on_warp_click_applied )
		self.figure.tsplot.warp_mouse_changed.connect( self.on_warp_mouse_changed )
		self.warp_controls.changed.connect( self.figure.tsplot.on_warp_control_widget_changed )
		
		
	def _initiate_using_prewarped_data(self, data):
		y0     = data.ydata_template
		y      = data.ydata_sources
		yw     = data.ydata_sources_warped
		
		J,Q    = y.shape
		self.label_nsources.setText( str(J) )
		self.spin_current_curve.setMaximum( J )

		#initialize figure:
		self.warp.set_domain_size(Q)
		self.figure._init(y0, y)
		self.figure.tsplot.set_warp(self.warp)
		
		for source,yy in zip(self.figure.tsplot.sources, yw):
			source.set_warped_ydata(yy)

		#callbacks:
		self.figure.tsplot.axes_entered.connect( self.on_axes_entered )
		self.figure.tsplot.curve_activated.connect( self.on_signal_curve_activated )
		self.figure.tsplot.warp_click_applied.connect( self.on_warp_click_applied )
		self.figure.tsplot.warp_mouse_changed.connect( self.on_warp_mouse_changed )
		self.warp_controls.changed.connect( self.figure.tsplot.on_warp_control_widget_changed )
		
		
	
	
	

	def _initiate_warp(self, caller='key_w'):
		if not self.figure.tsplot.iswarpactive:
			if self.figure.tsplot.active_object != self.figure.tsplot.template:
				if caller == 'key_w':
					self.figure.tsplot.initiate_warp_key_w()
					
				elif caller == 'button_init':
					# x   = self.warp_controls.get_position()
					control_params = self.warp_controls.get_value_dict()
					self.figure.tsplot.initiate_warp_button_inititate(control_params)
				
				self.enable_curve_selection(False)
				self.warp_controls.set_warp_enabled(True)
				self.figure.update_idle()
		


	def enable_curve_selection(self, enable=True):
		self.iscurveselectionenabled = enable
		self.button_next_curve.setEnabled( enable )
		self.button_previous_curve.setEnabled( enable )
		self.spin_current_curve.setEnabled( enable )
		self.figure.tsplot.enable_curve_selection(enable)


	
	def on_axes_entered(self):
		self.warp_controls.set_headtail_synced(True)
	
	
	def on_button_warp_applied(self):
		self.on_key_return()

	def on_button_warp_cancelled(self):
		self.on_key_escape()

	def on_button_warp_initiated(self):
		self._initiate_warp(caller='button_init')



	def on_key_escape(self):
		if self.figure.tsplot.iswarpactive:
			self.figure.tsplot.cancel_warp()
			self.figure.update_idle()
			self.enable_curve_selection()
			self.warp_controls.set_warp_enabled(False)
		

	def on_key_return(self):
		self.figure.tsplot.apply_warp()
		self.figure.update_idle()
		self.enable_curve_selection()
		self.warp_controls.set_warp_enabled(False)
		
		
		ind    = self.spin_current_curve.value() - 1
		source = self.figure.tsplot.active_object
		self.data.ydata_sources_warped[ind] = source.yw
		self.data.save()
		
		

	def on_key_o(self):
		if self.figure.tsplot.active_object != self.figure.tsplot.template:
			self.figure.tsplot.toggle_original_source_visibility()
			self.figure.update_idle()

	def on_key_r(self):
		if self.figure.tsplot.active_object != self.figure.tsplot.template:
			self.figure.tsplot.reset_warp()
			self.figure.update_idle()

	def on_key_s(self):
		self.figure.tsplot.toggle_unselected_visible()
		self.figure.update_idle()

	def on_key_t(self):
		self.figure.tsplot.toggle_template_visible()
		self.figure.update_idle()

	def on_key_w(self):
		self._initiate_warp(caller='key_w')
		


	def on_next_curve(self):
		if self.iscurveselectionenabled:
			self.figure.tsplot.set_next_selected()
			self.figure.update_idle()
		
	def on_previous_curve(self):
		if self.iscurveselectionenabled:
			self.figure.tsplot.set_previous_selected()
			self.figure.update_idle()
		
		


	def on_signal_curve_activated(self, ind):
		self.spin_current_curve.setValue( ind )
		self.warp_controls.button_initiate.setEnabled(ind!=0)
	
	def on_spin_current_curve(self, ind):
		if ind==0:
			self.figure.tsplot.set_template_active()
		else:
			self.figure.tsplot.set_source_active(ind-1)
		# print(ind)
		self.figure.update_idle()

	def on_warp_click_applied(self):
		self.figure.update_idle()
		self.enable_curve_selection()
		self.warp_controls.set_warp_enabled(False)


	def on_warp_mouse_changed(self):
		self.warp_controls.update_values_externally_changed()


	def set_data(self, data, prewarped=False):
		self.data = data
		if prewarped:
			self._initiate_using_prewarped_data(data)
		else:
			self._initiate_using_data(data)





if __name__ == '__main__':
	app    = QtWidgets.QApplication(sys.argv)
	widget = ManualPanel()
	widget.move(0, 0)
	widget.show()
	sys.exit(app.exec_())
