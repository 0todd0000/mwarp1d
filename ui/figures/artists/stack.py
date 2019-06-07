

from PyQt5 import QtWidgets, QtCore
from . _base import _SelectableArtist2D






class SelectionStack(_SelectableArtist2D):
	'''
	Thank you ImportanceOfBeingErnest!
	https://stackoverflow.com/questions/56015753/picking-a-single-artist-from-a-set-of-overlapping-artists-in-matplotlib
	'''
	
	empty_click          = QtCore.pyqtSignal(float, float)
	right_click_selected = QtCore.pyqtSignal(object, int)
	selected             = QtCore.pyqtSignal(object, int)
	point_dragged        = QtCore.pyqtSignal(object, int, int, float)
	
	def __init__(self, ax, stack=None):
		super().__init__(ax)
		self.stack    = [] if stack is None else stack

	def append(self, obj):
		self.stack.append(obj)
	
	def on_press(self, event):
		if event.inaxes:
			cont = [a for a in self.stack if a.isselectable and a.isvisible and a.h.contains(event)[0]]
			if cont:
				obj         = cont[0]
				ind         = obj.h.contains(event)[1]['ind']
				if event.button == 1:
					self.selected.emit(obj, min(ind) )
				elif event.button == 3:
					self.right_click_selected.emit(obj, min(ind))
			else:
				if event.button == 1:
					self.empty_click.emit( event.xdata, event.ydata )

	def on_selected(self, obj, ind):
		if self.notify:
			print(self.__class__.__name__ + ' selected', obj, ind)
		