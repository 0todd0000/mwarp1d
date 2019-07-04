

import sys,os
import numpy as np
from PyQt5 import QtWidgets, QtGui, QtCore



class VHeaderContextMenu(QtWidgets.QMenu):
	def __init__(self, parent, row):
		super().__init__(parent)
		menu     = QtWidgets.QMenu(self)
		label    = 'Unflag' if parent.rowflags[row] else 'Flag'
		a        = QtWidgets.QAction(label, self)
		a.triggered.connect( lambda: parent.toggle_flag(row) )
		menu.addAction(a)
		menu.popup( QtGui.QCursor.pos() )





class _LandmarksTable(QtWidgets.QTableWidget):
	def __init__(self, 	*args):
		super().__init__(*args)
		self.cellcolors = [QtGui.QColor(*x) for x in [(255,255,255), (200,200,200)]]
		self.fontcolors = [QtGui.QColor(*x) for x in [(200,200,200), (200,100,100), (50,150,50)]]
		

		
	def _build_table(self, update_counts=False):
		self.setRowCount( self.nrow )
		self.setColumnCount( self.ncol )
		[self.setColumnWidth(i, 50)  for i in range(self.ncol)]
		for i in range( self.nrow ):
			for ii in range( self.ncol ):
				item  = QtWidgets.QTableWidgetItem()
				item.setTextAlignment( QtCore.Qt.AlignCenter )
				self.setItem(i, ii, item)
				item.setText( str(self.A[i,ii]) )
				item.setFlags( QtCore.Qt.ItemIsEnabled )
		if update_counts:
			self.panel.update_counts()
		
		
	



	def _set_row_color(self, ind, c):
		for i in range(self.ncol):
			self.item(ind,i).setBackground( c )


	
	
	def delete_landmark(self, col):
		labels = self.get_landmark_names()
		labels.pop(col)
		self.A = np.hstack([self.A[:,:col], self.A[:,col+1:] ])
		self._build_table(update_counts=True)
		self.setHorizontalHeaderLabels( labels )

	def get_landmark_names(self):
		return [self.horizontalHeaderItem(c).text() for c in range(self.ncol)]



	def insert_landmark(self, col, x):
		i      = col
		z      = np.array([[x]*self.nrow], dtype=int).T
		labels = [self.horizontalHeaderItem(c).text() for c in range(self.ncol)]
		labels.insert(i, 'L')
		self.A = np.hstack([self.A[:,:i], z, self.A[:,i:] ])
		self._build_table(update_counts=True)
		self.setHorizontalHeaderLabels( labels )
		
		
		





	def rename_landmark(self, col):
		self.panel.rename_landmark(col)


	@QtCore.pyqtSlot(QtCore.QPoint)
	def on_vheader_rightclick(self, point):
		index = self.indexAt(point)
		row   = index.row()
		if row >0 :
			menu = VHeaderContextMenu(self, row)





	def on_vertical_header(self, index):
		if index>0:
			for i in range(1, self.nrow):
				self._set_row_color(i, self.cellcolors[0])
			self._set_row_color(index, self.cellcolors[1])


	@property
	def ncol(self):
		return self.A.shape[1]
	@property
	def nrow(self):
		return self.A.shape[0]
		
	def toggle_flag(self, row):
		self.rowflags[row] = not self.rowflags[row]



class LandmarksTableTemplate(_LandmarksTable):
	def _init(self, panel):
		self.panel      = panel
		self.A          = np.array([[25, 50, 75]])
		self._build_table()
		self.setHorizontalHeaderLabels(['L%d'%(i+1) for i in range(self.ncol)])
		self.horizontalHeader().sectionClicked.connect(self.panel.rename_landmark)
		self.setVerticalHeaderLabels(['___'])
		self.setVerticalScrollBarPolicy( QtCore.Qt.ScrollBarAlwaysOff )
		self.verticalHeaderItem(0).setForeground( QtGui.QBrush( QtGui.QColor( *[240]*3 )  ) )
		
		
		

		



class LandmarksTableSources(_LandmarksTable):
	def _init(self, panel):
		self.panel = panel
		n          = 8
		self.A     = np.vstack([[25]*n, [50]*n, [75]*n]).T
		self.rowflags   = [False]*self.nrow
		self._build_table()
		self.setHorizontalHeaderLabels( panel.get_landmark_names() )
		self.setVerticalHeaderLabels(['%03d'%(i+1)  for i in range(self.nrow)])
		
		self.horizontalHeader().sectionClicked.connect(self.panel.rename_landmark)
		vheader = self.verticalHeader()
		vheader.sectionClicked.connect(self.on_vertical_header)
		vheader.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		vheader.customContextMenuRequested.connect(self.on_vheader_rightclick)


