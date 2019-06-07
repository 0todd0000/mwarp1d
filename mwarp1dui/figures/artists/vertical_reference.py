

class VerticalReference(object):
	def __init__(self, ax, visible=True):
		self.ax    = ax
		self.vl    = ax.axvline(0, color=(0.6,0.9,0.6), ls='-')
		self.vl.set_visible(visible)
	
	def set_visible(self, visible=True):
		self.vl.set_visible(visible)
	
	def set_x_position(self, x):
		self.vl.set_xdata([x,x])


