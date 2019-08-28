
import sys,os
import numpy as np
from PyQt5 import QtWidgets, QtGui, QtCore, uic
import numpy as np


class _LandmarksTableModel(QtCore.QAbstractTableModel):
	
	firstrow   = 1
	
	def __init__(self, landmarks, parent=None, labels=None):
		super().__init__(parent)
		self.landmarks  = landmarks
		self.collabels  = ['C%d'%(i+1)  for i in range( self.ncols )] if (labels is None) else labels
		self.nullvalues = False
	
	
	@property
	def ncols(self):
		return self.landmarks[0].n
	@property
	def nrows(self):
		return len(self.landmarks)
	
	
	
	def columnCount(self, parent):
		return self.ncols

	def rowCount(self, parent):
		return self.nrows
	
	def data(self, index, role):
		if not index.isValid():
			return None

		row,col  = index.row(), index.column()

		if role in [QtCore.Qt.DisplayRole, QtCore.Qt.EditRole]:
			# self.dataChanged.emit(index, index, (QtCore.Qt.DisplayRole, ))
			if self.nullvalues:
				return '-'
			else:
				return str( self.landmarks[row].h.get_xdata()[col] )
			
		elif role == QtCore.Qt.TextAlignmentRole:
			return QtCore.Qt.AlignCenter

		elif (role == QtCore.Qt.DecorationRole) and (col==0):
			return ""

		elif (role == QtCore.Qt.ToolTipRole) and (col==0):
			return ""
			

	def headerData(self, section, orientation, role):
		if role == QtCore.Qt.DisplayRole:
			if orientation == QtCore.Qt.Horizontal: 
				return self.collabels[section]
			elif orientation == QtCore.Qt.Vertical:
				return str(section+self.firstrow)
				
		elif role == QtCore.Qt.ForegroundRole:
			if orientation == QtCore.Qt.Vertical:
				if self.landmarks[section].isflagged:
					return QtGui.QBrush(QtCore.Qt.red)
				else:
					return QtGui.QBrush(QtCore.Qt.black)
		










class _LandmarksTable(QtWidgets.QTableView):
	colname_changed    = QtCore.pyqtSignal(int, str)
	rows_selected      = QtCore.pyqtSignal(list)
	

	colors_enabled     = dict(background=QtGui.QColor(*[235]*3), emptyspace=QtGui.QColor(*[250]*3), headers=QtGui.QColor(*[220]*3), text=QtGui.QColor(*[10]*3))
	colors_disabled    = dict(background=QtGui.QColor(*[130]*3), emptyspace=QtGui.QColor(*[135]*3), headers=QtGui.QColor(*[120]*3), text=QtGui.QColor(*[160]*3))
	# color_enabled      = QtGui.QColor(200,200,200)
	# color_disabled     = QtGui.QColor(50,50,50)
	
	column_width       = 60

	ModelClass         = _LandmarksTableModel

	def _init(self, landmarks, labels=None):
		### set model:
		self.model    = self.ModelClass(landmarks, self, labels)
		self.proxy    = QtCore.QSortFilterProxyModel(self)
		self.proxy.setSourceModel(self.model)
		self.setModel(self.proxy)
		# self.setUpdatesEnabled(True)

		# ### set row flags:
		# self.rowflags = [False]*self.nrows

		### column widths:
		# self._set_column_widths()


		### selected row colors:
		self.setSelectionBehavior( QtWidgets.QAbstractItemView.SelectRows )
		self.setSelectionMode( QtWidgets.QAbstractItemView.SingleSelection )
		
		self.pal = QtGui.QPalette()
		self.pal.setColor( QtGui.QPalette.Highlight, QtGui.QColor(200,200,200) )
		self.pal.setColor( QtGui.QPalette.HighlightedText, QtGui.QColor(255,255,255) )
		self.setPalette(self.pal)

		self.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
		self.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
		
		self.set_column_widths()
		


		### header callbacks:
		# self.horizontalHeader().sectionClicked.connect(self.rename_column)
		# vheader = self.verticalHeader()
		# vheader.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		# vheader.customContextMenuRequested.connect(self.on_vheader_rightclick)





	def _get_selected_rows(self):
		return [sr.row() for sr in self.selectionModel().selectedRows()]

	# def _set_column_widths(self):
	# 	[self.setColumnWidth(i, 50)  for i in range(self.ncol)]

	@property
	def ncols(self):
		return self.model.ncols
	@property
	def nrows(self):
		return self.model.nrows


	def add_column(self, ind):
		self.model.beginInsertColumns(QtCore.QModelIndex(), self.ncols-1, self.ncols-1)
		self.model.collabels.insert(ind, 'C')
		self.model.endInsertColumns()
		self.set_column_widths()
		self.repaint()

		
	def delete_column(self, ind):
		self.model.beginRemoveColumns(QtCore.QModelIndex(), ind, ind)
		self.model.collabels.pop(ind)
		self.model.endRemoveColumns()
		self.repaint()
		
		# self.model.removeColumn(ind)
		# self.model.collabels.pop(ind)
		# self.model.headerDataChanged.emit(QtCore.Qt.Horizontal, ind, ind)
		# self.repaint()
		

	# def on_vheader_leftclick(self, index):
	# 	rows = self._get_selected_rows()
	# 	self.rows_selected.emit(rows)


	def enable(self, enabled):
		self.setEnabled( enabled )
		c   = self.colors_enabled if enabled else self.colors_disabled
		pal = QtGui.QPalette()
		pal.setColor(QtGui.QPalette.Background, c['background'])
		pal.setColor(QtGui.QPalette.Base, c['emptyspace'])
		pal.setColor(QtGui.QPalette.Button, c['headers'])
		pal.setColor(QtGui.QPalette.Text, c['text'])
		pal.setColor(QtGui.QPalette.ButtonText, c['text'])
		self.setPalette(pal)
		self.repaint()



	def get_landmark_names(self):
		return self.model.collabels

	def get_table_as_array(self):
		a = np.array([lm.h.get_xdata() for lm in self.model.landmarks])
		return a if self.nrows>1 else a[0]

	def rename_column(self, col):
		s0  = self.model.collabels[col]
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
			if s != s0:
				# self.colname_changed.emit(col, s)
				self.set_collabel(col, s)
				self.colname_changed.emit(col, s)
				# self.model.collabels[col] = s

	def set_cell_value(self, row, col, value):
		index  = self.model.index(row, col)
		self.model.setData(index, value)
		self.model.dataChanged.emit(index, index, (QtCore.Qt.DisplayRole, ))

	def set_column_widths(self):
		[self.setColumnWidth(i, self.column_width) for i in range(self.ncols)]
	
	def set_row_values(self, row, values):
		for i,x in enumerate(values):
			index  = self.model.index(row, i)
			self.model.setData(index, x)
		self.model.dataChanged.emit(index, index, (QtCore.Qt.DisplayRole, ))

	def set_collabel(self, col, s):
		self.model.collabels[col] = s
	
	
	def set_null_values(self, null=True):
		self.model.nullvalues = null
	
	def update(self):
		# index = QtCore.QModelIndex()
		# self.model.dataChanged.emit(index, index, (QtCore.Qt.DisplayRole, ))
		# self.model.layoutChanged.emit()
		pass




