
import sys,os
import numpy as np
from PyQt5 import QtWidgets, QtGui, QtCore, uic
import numpy as np


from . _base import _LandmarksTable, _LandmarksTableModel


class VHeaderContextMenu(QtWidgets.QMenu):
	def __init__(self, parent, rows):
		super().__init__(parent)
		menu     = QtWidgets.QMenu(self)
		if len(rows) < 2:
			row      = rows[0]
			# label    = 'Unflag' if parent.rowflags[row] else 'Flag'
			label    = 'Unflag' if parent.model.landmarks[row].isflagged else 'Flag'
			a        = QtWidgets.QAction(label, self)
			a.triggered.connect( lambda: parent.toggle_flag(row) )
			menu.addAction(a)
			menu.popup( QtGui.QCursor.pos() )
		else:
			s0,s1     = 'Flag all', 'Unflag all'
			a0,a1     = QtWidgets.QAction(s0, self), QtWidgets.QAction(s1, self)
			a0.triggered.connect( lambda: parent.flag_rows(rows) )
			a1.triggered.connect( lambda: parent.unflag_rows(rows) )
			menu.addAction(a0)
			menu.addAction(a1)
			menu.popup( QtGui.QCursor.pos() )



class SourceTableModel(_LandmarksTableModel):
	pass




class SourceTable(_LandmarksTable):
	
	ModelClass            = SourceTableModel
	
	rowflags_changed      = QtCore.pyqtSignal()
	
	
	def _init(self, landmarks, labels=None):
		super()._init(landmarks, labels)
		# self.horizontalHeader().setEnabled(False)
		vheader = self.verticalHeader()
		vheader.sectionClicked.connect(self.on_vheader_leftclick)
		vheader.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		vheader.customContextMenuRequested.connect(self.on_vheader_rightclick)
		


	def flag_rows(self, rows):
		for row in rows:
			self.model.landmarks[row].set_flagged(True)
		self.model.headerDataChanged.emit( QtCore.Qt.Vertical, rows[0], rows[-1])
		self.rowflags_changed.emit()


	def toggle_flag(self, row):
		self.model.landmarks[row].toggle_flag()
		self.model.headerDataChanged.emit( QtCore.Qt.Vertical, row, row)
		self.rowflags_changed.emit()


	def unflag_rows(self, rows):
		for row in rows:
			self.model.landmarks[row].set_flagged(False)
		self.model.headerDataChanged.emit( QtCore.Qt.Vertical, rows[0], rows[-1])
		self.rowflags_changed.emit()

	
	def on_vheader_leftclick(self, index):
		rows = self._get_selected_rows()
		self.rows_selected.emit(rows)


	@QtCore.pyqtSlot(QtCore.QPoint)
	def on_vheader_rightclick(self, point):
		pass
		# selected_rows = self._get_selected_rows()
		# row           = self.indexAt(point).row()
		# if row not in selected_rows:
		# 	selected_rows.append(row)
		# menu  = VHeaderContextMenu(self, selected_rows)



