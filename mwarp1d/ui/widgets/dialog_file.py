

from PyQt5 import QtWidgets, QtCore


class FileSaveDialog(QtWidgets.QFileDialog):
	def __init__(self, ext=None):
		super().__init__()
		self.setWindowTitle('aaaaaBBBBcccc')
		self.setFilter(self.filter() | QtCore.QDir.Hidden)
		if ext is not None:
			self.setDefaultSuffix(ext)
		self.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)
		self.setNameFilters(   [ '%s (*.%s)' %(ext.upper(), ext) ]   )






	