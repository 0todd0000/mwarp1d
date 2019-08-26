
from PyQt5 import QtWidgets, QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from . artists import TemplateSourcePlotManual




class _Figure(FigureCanvas):
	def __init__(self, parent=None):
		self.figure = Figure(dpi=100)
		self.ax     = self.figure.add_axes([0,0,1,1])
		super().__init__(self.figure)
		self.setParent(parent)
		super().setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		super().updateGeometry()
		self.setFocusPolicy( QtCore.Qt.ClickFocus )
		self.setFocus()
		
		policy = self.sizePolicy()
		policy.setRetainSizeWhenHidden(True)
		self.setSizePolicy(policy)

	def set_visible(self, visible):
		self.setVisible(visible)
		






class FigureManual(_Figure):
	
	def __init__(self, parent=None):
		super().__init__(parent)
		self.J              = None
		self.Q              = None
		self.tsplot         = None

	def _init(self, template, sources):
		J,Q               = sources.shape
		self.J            = J
		self.Q            = Q
		ytemplate         = np.random.randn(101) if (template is None) else template
		ysources          = np.random.randn(8,101) if (sources is None) else sources
		self.tsplot       = TemplateSourcePlotManual(self.ax, self.Q)
		self.tsplot.set_template( ytemplate )
		self.tsplot.set_sources( sources )
		self.tsplot.init_legend()
		self.tsplot.template.set_active(True)
		self.ax.figure.canvas.draw()
		

	def reset(self):
		self.ax.figure.clf()
		self.ax     = self.figure.add_axes([0,0,1,1])
		self.ax.figure.canvas.draw()
		self.tsplot = None
		

	def update_idle(self):
		self.ax.figure.canvas.draw_idle()

