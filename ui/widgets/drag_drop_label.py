#!/usr/bin/env python

import os
from PyQt5 import QtWidgets, QtCore


class DragDropLabel(QtWidgets.QLabel):
	
	files_dropped = QtCore.pyqtSignal(list)

	def __init__(self, parent):
		super().__init__(parent)
		self.setAcceptDrops(True)


	def dragEnterEvent(self, e):
		if e.mimeData().hasUrls() and len(e.mimeData().urls())<=2:
			e.accept()
			fname = e.mimeData().urls()[0].toLocalFile()
			if os.path.splitext(fname)[1].upper() in ['.CSV', '.NPZ']:
				self.set_color(1)
			else:
				self.set_color(2)
		else:
			e.ignore()

	def dragLeaveEvent(self, e):
		self.set_color(0)
		

	def dropEvent(self, e):
		filenames = [url.toLocalFile() for url in e.mimeData().urls()]
		self.files_dropped.emit(filenames)

	def set_color(self, color_code):
		if color_code == 0:
			self.setStyleSheet('background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(150, 150, 150, 255), stop:1 rgba(200, 200, 200, 255));')
		elif color_code == 1:
			self.setStyleSheet('background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(150, 210, 150, 255), stop:1 rgba(200, 200, 200, 255));')
		else:
			self.setStyleSheet('background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(210, 150, 150, 255), stop:1 rgba(200, 200, 200, 255));')

	