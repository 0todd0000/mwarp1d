
import sys,os
import numpy as np
from PyQt5 import QtWidgets, QtGui, QtCore, uic
import numpy as np

from . _base import _LandmarksTable, _LandmarksTableModel


class TemplateTableModel(_LandmarksTableModel):
	
	firstrow = 0
	
	@property
	def nrows(self):
		return 1
	




class TemplateTable(_LandmarksTable):
	
	ModelClass                  = TemplateTableModel
	template_table_row_selected = QtCore.pyqtSignal()
	
	
	def _init(self, A, labels=None):
		super()._init(A, labels)
		# self.setSelectionMode( QtWidgets.QAbstractItemView.NoSelection )
		self.horizontalHeader().sectionClicked.connect(self.rename_column)
		# self.verticalHeader().setEnabled(False)
		self.verticalHeader().sectionClicked.connect(self.on_vheader_leftclick)

	def add_column(self, ind):
		super().add_column(ind)
		# self.model.beginInsertColumns(QtCore.QModelIndex(), self.ncols-1, self.ncols-1)
		# self.model.collabels.insert(ind, 'C')
		# self.model.endInsertColumns()
		# self.set_column_widths()
		self.verticalHeader().sectionPressed.emit(0)
	
	def on_vheader_leftclick(self, index):
		self.template_table_row_selected.emit()


	def set_landmarks_object(self, obj):
		self.landmarks   = obj
		
		
	# def update_table(self):
	# 	self.model.dataChanged.emit(index, index, (QtCore.Qt.DisplayRole, ))




