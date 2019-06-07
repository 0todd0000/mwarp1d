
import numpy as np
from . _base import _SelectableArtist2D


class _SelectableLine(_SelectableArtist2D):
	linewidth          = 0.5
	
	def __init__(self, ax, y, collection=None):
		super().__init__(ax, collection)
		self.Q        = y.size
		self.h        = self.ax.plot(y, '-', lw=self.linewidth, color=self.color_active, zorder=self.zorder)[0]


class Source(_SelectableLine):
	linewidth          = 0.5
	zorder             = 0

class Template(_SelectableLine):
	linewidth          = 5
	zorder             = 2


	