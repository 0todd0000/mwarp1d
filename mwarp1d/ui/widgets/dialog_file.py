

from PyQt5 import QtWidgets, QtCore


class FileSaveDialog(QtWidgets.QFileDialog):
	def __init__(self, ext=None, dir=None):
		super().__init__()
		self.setFilter(self.filter() | QtCore.QDir.Hidden)
		if dir is not None:
			self.setDirectory(dir)
		if ext is not None:
			self.setDefaultSuffix(ext)
		self.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)
		self.setNameFilters(   [ '%s (*.%s)' %(ext.upper(), ext) ]   )






	