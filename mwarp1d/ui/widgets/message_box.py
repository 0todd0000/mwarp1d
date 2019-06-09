

from PyQt5 import QtWidgets



class MessageBox(QtWidgets.QMessageBox):
	def __init__(self, s='Message'):
		super().__init__()
		self.setIcon( QtWidgets.QMessageBox.Information )
		self.setText( s )
		self.setWindowTitle( 'MWarp1D Messgae' )
		self.setStandardButtons(QtWidgets.QMessageBox.Ok)
		returnValue = self.exec()
		# if returnValue == QtWidgets.QMessageBox.Ok:
		# 	pass


	