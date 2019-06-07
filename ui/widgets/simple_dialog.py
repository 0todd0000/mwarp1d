

from PyQt5 import QtWidgets



class SimpleDialog(QtWidgets.QMessageBox):
	def __init__(self, s='Message'):
		super().__init__()
		self.setIcon( QtWidgets.QMessageBox.Warning )
		self.setText( s )
		self.setWindowTitle( 'MWarp1D Messgae' )
		self.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
		
	def exec(self):
		response = super().exec()
		return response==QtWidgets.QMessageBox.Ok
		
		


	