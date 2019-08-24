#!/usr/bin/env python

import os
from PyQt5 import QtWidgets, QtCore


class ClickableLabel(QtWidgets.QLabel):
	
	clicked = QtCore.pyqtSignal()

	def __init__(self, parent):
		super().__init__(parent)

	def enterEvent(self, e):
		self.setCursor( QtCore.Qt.PointingHandCursor )

	def leaveEvent(self, e):
		pass

	def mousePressEvent(self, e):
		self.clicked.emit()


