
from PyQt5 import QtWidgets, QtCore
from . selectable_line import Template,Source
from . draggable_points import TemplateLandmarks,SourceLandmarks
from . stack import SelectionStack




class _LinePointCollection(QtCore.QObject):
	
	LandmarksClass    = TemplateLandmarks
	LineClass         = Template
	point_deleted     = QtCore.pyqtSignal(object, int)
	selected          = QtCore.pyqtSignal(object, int)
	
	
	def __init__(self, ax, y):
		super().__init__()
		self.ax        = ax
		self.line      = self.LineClass(ax, y, collection=self)
		self.h         = self.line.h
		self.landmarks = None
		self.stack     = None
		
	def add_landmark(self, x):
		self.landmarks.add_point(x)


	def get_line_x(self):
		return self.line.get_xdata()
	def get_line_y(self):
		return self.line.get_ydata()
	
	
	@property
	def isvisible(self):
		return self.line.isvisible
	
	
	def on_point_deleted(self, ind):
		self.point_deleted.emit(self.landmarks, ind)
	
	def set_landmarks(self, x):
		self.landmarks = self.LandmarksClass(self.ax, x, y_constraint=self.get_line_y(), collection=self)
		
		self.stack     = SelectionStack(self.ax, [self.landmarks, self.line])

		self.line.set_notify(False)
		self.landmarks.set_notify(False)
		self.stack.set_notify(True)
		
		self.selected   = self.stack.selected
		self.landmarks.point_deleted.connect( self.on_point_deleted )


	def set_active(self, active):
		self.line.set_active(active)
		if self.landmarks is not None:
			self.landmarks.set_active(active)


	def set_notify(self, notify):
		self.stack.set_notify(notify)
		
	def set_visible(self, visible):
		self.landmarks.set_visible(visible)
		self.line.set_visible(visible)
		




class SourceWithLandmarks(_LinePointCollection):
	LandmarksClass    = SourceLandmarks
	LineClass         = Source
	
	def calculate_mse(self, template):
		y0 = template.line.h.get_ydata()
		y  = self.h.get_ydata()
		return ((y-y0)**2).mean()
	



class TemplateWithLandmarks(_LinePointCollection):
	LandmarksClass    = TemplateLandmarks
	LineClass         = Template
	


	