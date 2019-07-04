#!/usr/bin/env python

# import sys,os
from math import floor
from PyQt5 import QtWidgets, QtCore, uic
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import numpy as np
from . artists import TemplateSourcePlot




class _Figure(FigureCanvas):
	def __init__(self, parent=None):
		self.figure = Figure(dpi=100)
		self.ax     = self.figure.add_axes([0,0,1,1])
		super().__init__(self.figure)
		self.setParent(parent)
		super().setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		super().updateGeometry()
		self.setFocusPolicy( QtCore.Qt.ClickFocus )
		self.setFocus()
		
		policy = self.sizePolicy()
		policy.setRetainSizeWhenHidden(True)
		self.setSizePolicy(policy)

	def set_visible(self, visible):
		self.setVisible(visible)
		


class FigureLandmarksRegistered(_Figure):
	
	color_source_selected    = (1, 0.56, 0)
	color_source_unselected  = '0.7'
	
	
	def _init(self, y0=None, y=None):
		self.y0           = np.random.randn(101) if (y0 is None) else y0
		self.y            = np.random.randn(8,101) if (y is None) else y
		self.h0           = self.ax.plot(self.y0,  lw=4,   color='k')[0]
		self.h            = self.ax.plot(self.y.T, lw=0.5, color=self.color_source_unselected)

	def clear_source_selection(self, update=True):
		for h in self.h:
			h.set_color( self.color_source_unselected )
			h.set_linewidth(0.5)
		if update:
			self.ax.figure.canvas.draw()
	
	def plot(self, y):
		self.ax.plot( y.T )

	def get_warped_sources_as_array(self):
		return np.array([hh.get_ydata()  for hh in self.h])
	
	def set_source_selected(self, ind):
		self.clear_source_selection(update=False)
		self.h[ind].set_color( self.color_source_selected )
		self.h[ind].set_linewidth( 1 )
		self.ax.figure.canvas.draw()
		
	def set_sources_visible(self, visible):
		[h.set_visible(visible) for h in self.h]
		
	def set_sources_visible_bool_list(self, visible):
		for h,v in zip(self.h, visible):
			h.set_visible(v)
			
			
	def set_template_visible(self, visible):
		self.h0.set_visible( visible )





class FigureLandmarks(_Figure):
	
	landmark_deleted                     = QtCore.pyqtSignal(int)
	
	
	
	def __init__(self, parent=None):
		super().__init__(parent)
		self.J              = None
		self.Q              = None
		self.tsplot         = None

	
	
	def _init(self, template, sources, lmtemplate=None, lmsources=None):
		J,Q               = sources.shape
		self.J            = J
		self.Q            = Q
		ytemplate         = np.random.randn(101) if (template is None) else template
		ysources          = np.random.randn(8,101) if (sources is None) else sources
		lmtemplate        = [25, 50, 75] if (lmtemplate is None) else lmtemplate
		lmsources         = np.vstack([[25]*J, [50]*J, [75]*J]).T if (lmsources is None) else lmsources
		
		self.tsplot       = TemplateSourcePlot(self.ax, self.Q)
		self.tsplot.set_template( ytemplate, lmtemplate )
		self.tsplot.set_sources( ysources, lmsources )
		self.tsplot.init_legend()

		self.tsplot.point_deleted.connect(self.on_point_deleted)
		
		
		self.curve_left_click_selected    = self.tsplot.curve_left_click_selected
		self.curve_arrow_selected         = self.tsplot.curve_arrow_selected
		self.dragging_stopped             = self.tsplot.dragging_stopped
		self.template_point_dragged       = self.tsplot.template_point_dragged
		self.source_point_dragged         = self.tsplot.source_point_dragged
		self.template_landmark_added      = self.tsplot.template_landmark_added
		self.toggle_unselected_visible    = self.tsplot.toggle_unselected_visible
		self.update_flagged_source_colors = self.tsplot.update_flagged_source_colors
		
		self.maxlandmarksreached       = self.tsplot.maxlandmarksreached
		
		self.get_active_source         = self.tsplot.get_active_source
		self.reset_source_landmarks    = self.tsplot.reset_source_landmarks
		self.set_template_active       = self.tsplot.set_template_active
		self.set_template_landmark_adding_enabled        = self.tsplot.set_template_landmark_adding_enabled
		self.set_template_landmark_dragging_enabled      = self.tsplot.set_template_landmark_dragging_enabled
		
		
		
	def get_source_landmarks_objects(self):
		return [s.landmarks for s in self.tsplot.sources]

	def get_template_landmarks_object(self):
		return self.tsplot.template.landmarks
	
	
	def on_point_deleted(self, obj, ind):
		self.landmark_deleted.emit(ind)


	def set_next_selected(self):
		self.tsplot.set_next_selected()
		# self.curve_selected.emit()
	def set_previous_selected(self):
		self.tsplot.set_previous_selected()
	def select_source(self, ind):
		self.tsplot.set_source_active(ind)
	def select_source_by_table_header_click(self, ind):
		self.tsplot.set_source_active(ind)
	
	def set_source_landmarks_visible(self, visible):
		[source.landmarks.set_visible(visible) for source in self.tsplot.sources]

	def set_sources_visible(self, visible):
		[source.set_visible(visible) for source in self.tsplot.sources]

	
	
	
	def set_template_locked(self, locked):
		self.set_template_landmark_adding_enabled(not locked)
		self.set_template_landmark_dragging_enabled(not locked)
		self.set_sources_visible(locked)
		self.set_source_landmarks_visible(False)
		self.ax.figure.canvas.draw()
		
	
	def set_template_selected(self):
		self.tsplot.set_template_active()
		
		

	def set_template_visible(self, visible):
		self.tsplot.set_template_visible(visible)
		
		
	


