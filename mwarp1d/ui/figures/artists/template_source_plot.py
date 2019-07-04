#!/usr/bin/env python

from math import floor
from PyQt5 import QtWidgets, QtCore
import numpy as np
from . import Crosshairs
from . import SelectionStack
from . import SourceWithLandmarks, TemplateWithLandmarks
from . import Source,Template
from . import SourceLandmarks, TemplateLandmarks





class TemplateSourcePlot(QtCore.QObject):
		
	curve_arrow_selected      = QtCore.pyqtSignal(int)
	curve_left_click_selected = QtCore.pyqtSignal(int)
	dragging_stopped          = QtCore.pyqtSignal()
	empty_click               = QtCore.pyqtSignal(float, float)
	point_deleted             = QtCore.pyqtSignal(object, int)
	source_point_dragged      = QtCore.pyqtSignal(int, int, int, float)
	template_point_dragged    = QtCore.pyqtSignal(int, int, float)
	template_landmark_added   = QtCore.pyqtSignal(int, int)
	
	
	is_unselected_visible     = True
	is_warped_visible         = True
	
	
	def __init__(self, ax, Q):
		super().__init__()
		# self._hw                 = None
		self._sources0           = None
		self._sourcesw           = None
		self.Q                   = Q
		self.ax                  = ax
		self.dragging_stopped_emitted = False
		self.stack               = SelectionStack(ax)
		self.crosshairs          = Crosshairs(ax, visible=False)
		self.sources             = None
		self.template            = None
		self.selected_object = None
		self.stack.set_notify(False)
		self.stack.selected.connect( self.on_left_click_selected )
		self.ax.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)
		self.ax.figure.canvas.mpl_connect('figure_leave_event', self.on_leave)
		
		
		self.stack.empty_click.connect(self.on_empty_click)
		self.stack.right_click_selected.connect(self.on_right_click_selected)
		# self.stack.point_dragged.connect( self.on_point_dragged )
		
		self.maxlandmarksreached = None
		self.template_landmark_adding_enabled = True
		
		
	
	@property
	def J(self):
		return None if (self.sources is None) else len(self.sources)


	def add_landmark(self):
		x = self.crosshairs.get_xpos()
		x = floor(self.Q/2) if x is None else x
		if x is not None:
			if self.selected_object == self.template and self.template.isvisible:
				ind   = floor(x)
				if (ind > -1) and (ind < self.Q-1):
					self.template.add_landmark(ind)
	
	
	def get_active_source(self):
		sources = [s for s in self.sources if s.line.isactive]
		return sources[0] if len(sources)>0 else None
	
	
	def get_source_by_selected_object(self, obj):
		for i,s in enumerate(self.sources):
			if (obj==s.line) or (obj==s.landmarks):
				return i,s


	def init_legend(self):
		h0,h1      = self.template.h, self.sources[0].h
		self.leg   = self.ax.legend([h0,h1], ['Template', 'Source'], loc='upper left')

		
	def on_empty_click(self, x, y):
		self.empty_click.emit(x, y)
		if self.template_landmark_adding_enabled:
			if self.selected_object == self.template and self.template.isvisible:
				ind   = floor(x)
				if (ind > -1) and (ind < self.Q-1):
					self.template.add_landmark(ind)
		
		
	def on_leave(self, event):
		self.crosshairs.set_visible(False)
		self.update()

	
	def on_dragging_stopped(self):
		if not self.dragging_stopped_emitted:
			self.dragging_stopped.emit()
			self.dragging_stopped_emitted = True
	
	def on_motion(self, event):
		if event.inaxes:
			self.crosshairs.set_visible(True)
			self.crosshairs.set_xdata( event.xdata )
			self.ax.figure.canvas.draw()
		else:
			self.crosshairs.set_visible(False)
			self.ax.figure.canvas.draw()
		# print( self.template.landmarks.h.get_xdata() )
	
	

	def on_template_landmark_added(self, ind, value):
		# print('TemplateSourcePlot on_template_landmark_added', ind, value)
		self.template_landmark_added.emit(ind, value)


	def on_landmark_dragged(self, obj, ind, x, y):
		# print(obj, ind, x, y)
		self.dragging_stopped_emitted = False
		if obj == self.template.landmarks:
			self.template_point_dragged.emit(ind, x, y)
			

			
			
		else:
			sourceind = self.get_source_by_selected_object(obj)[0]
			self.source_point_dragged.emit(sourceind, ind, x, y)

	
	def on_right_click_selected(self, obj, ind):
		if isinstance(obj, TemplateLandmarks):
			deleted = obj.delete_point(ind)
			if deleted:
				self.point_deleted.emit(obj, ind)
			
		
	
	def on_left_click_selected(self, obj, ind):
		self.set_all_active(False)
		if isinstance(obj, (Template,TemplateLandmarks)):
			self.template.set_active(True)
			self.selected_object = self.template
			self.curve_left_click_selected.emit(0)
		elif isinstance(obj, (Source,SourceLandmarks)):
			ind,source = self.get_source_by_selected_object(obj)
			self.curve_left_click_selected.emit( ind+1 )
			self.selected_object = source
			source.set_active(True)
			
			self.ax.figure.canvas.draw()
		self.ax.figure.canvas.draw()
	
	
	
	def reset_source_landmarks(self):
		x = self.template.landmarks.values
		[source.landmarks.set_all_xdata(x.copy())  for source in self.sources]
	
	





	def set_all_active(self, active=True):
		self.template.set_active(active)
		[s.set_active(active) for s in self.sources]

	

	def set_next_selected(self):
		if self.selected_object == self.template:
			self.set_source_active(0)
			self.curve_arrow_selected.emit(1)
		else:
			ind  = self.sources.index( self.selected_object )
			if ind == self.J-1:
				self.set_template_active()
				self.curve_arrow_selected.emit(0)
			else:
				self.set_source_active(ind+1)
				self.curve_arrow_selected.emit(ind+2)
		self.set_unselected_visible( self.is_unselected_visible )
		
		
	def set_previous_selected(self):
		if self.selected_object == self.template:
			self.set_source_active(self.J-1)
			self.curve_arrow_selected.emit(self.J)
		else:
			ind  = self.sources.index( self.selected_object )
			
			if ind == 0:
				self.set_template_active()
				self.curve_arrow_selected.emit(0)
			else:
				self.set_source_active(ind-1)
				self.curve_arrow_selected.emit(ind)
		self.set_unselected_visible( self.is_unselected_visible )

		
		
	

	def set_source_active(self, ind):
		self.set_all_active(False)
		self.sources[ind].set_active(True)
		self.selected_object = self.sources[ind]
		# self.curve_left_click_selected.emit(ind+1)
		self.update()


	def set_sources(self, y, x):
		if self.sources is None:
			self.sources   = []
			self._sources0 = y.copy()
			self._sourcesw = y.copy()
			landmarks      = []
			lines          = []
			for xx,yy in zip(x,y):
				source = SourceWithLandmarks(self.ax, yy)
				source.set_landmarks(xx)
				source.set_active(False)
				source.set_notify(False)
				source.landmarks.dragged.connect( self.on_landmark_dragged )
				source.landmarks.dragging_stopped.connect( self.on_dragging_stopped )
				landmarks.append( source.landmarks )
				lines.append( source.line )
				self.sources.append(source)
			[self.stack.append(x) for x in landmarks]
			[self.stack.append(x) for x in lines]
			

	def set_template(self, y, x):
		if self.template is None:
			self.template = TemplateWithLandmarks(self.ax, y)
			self.template.set_landmarks(x)
			self.template.set_notify(False)
			self.stack.append( self.template.landmarks )
			self.stack.append( self.template.line )
			self.selected_object = self.template
			
			self.template.landmarks.dragged.connect( self.on_landmark_dragged )
			self.template.landmarks.point_added.connect( self.on_template_landmark_added )
			
			self.maxlandmarksreached = self.template.landmarks.maxpointsreached
			

	def set_template_active(self):
		self.set_all_active(False)
		self.template.set_active(True)
		self.selected_object = self.template
		self.update()


	def set_template_landmark_dragging_enabled(self, enabled):
		self.template.landmarks.set_dragging_enabled(enabled)

	def set_template_landmark_adding_enabled(self, enabled):
		self.template_landmark_adding_enabled = enabled


	def set_template_visible(self, visible):
		if self.selected_object == self.template:
			self.template.set_visible(visible)
			self.template.set_active(False)
			self.set_source_active(0)
		else:
			self.template.set_visible(visible)
			self.update()

	
	def set_unselected_visible(self, visible):
		for source in self.sources:
			if source.line.isactive:
				source.landmarks.set_visible( True )
				source.line.set_visible( True )
			else:
				source.landmarks.set_visible( False )
				source.line.set_visible( visible )
		self.ax.figure.canvas.draw()
		
	
	
	def toggle_legend_visible(self):
		self.leg.set_visible( not self.leg.get_visible() )
		self.ax.figure.canvas.draw()


	def toggle_unselected_visible(self):
		self.is_unselected_visible = not self.is_unselected_visible
		self.set_unselected_visible( self.is_unselected_visible )
		
	
	
	def update(self):
		self.ax.figure.canvas.draw()


	def update_flagged_source_colors(self):
		for source in self.sources:
			flagged = source.landmarks.isflagged
			source.line.set_flagged(flagged)
			source.landmarks.update_colors()
			source.line.update_colors()


