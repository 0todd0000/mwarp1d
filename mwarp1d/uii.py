
'''
functions and classes for interfacing with the UI via scripting
'''

import numpy as np
from . manual import ManualWarp1D, SequentialManualWarp



def launch_gui(data=None, mode=None, filename_results=None, filename_data=None):
	'''
	Command-line access to GUI launching.
	
	This function allows the user to bypass the initial GUI screen and proceed
	directly to the specified warping interface, thereby avoiding manual GUI setup.
	
	This function can be called from both Python and interactive Python. The GUI will
	be launched as a subprocess of the active Python kernel.
	
	:Keyword args:
		
		**data** --- a 2D NumPy array (rows = observations, columns = domain nodes)
		
		**mode** --- "landmark" or "manual"
		
		**filename_results** --- file name (zipped NumPy format, with extension "npz") into which warping results will be saved

		**filename_data** --- CSV file name, formatted as "data" above (data or filename_data can be specified, but not both)
	'''
	import os
	narg        = 0
	
	# assert input argument types:
	if data is not None:
		assert isinstance(data, np.ndarray), '"data" must be a numpy array'
		assert data.ndim==2, '"data" must be a 2-D numpy array'
		narg   += 1
	if mode is not None:
		modes   = ['landmark', 'manual']
		assert mode in modes, '"mode" must be "landmark" or "manual"'
		narg   += 1
	if filename_results is not None:
		msg     = '"filename_results" must be a valid filename with the extension ".npz"'
		try:
			ext = os.path.splitext(filename_results)[1]
			assert ext == '.npz', msg
		except:
			raise ValueError(msg)
		narg   += 1
	if filename_data is not None:
		msg     = '"filename_data" must be an existing data file name with the extension ".csv"'
		try:
			ext = os.path.splitext(filename_data)[1]
			assert ext == '.csv', msg
			assert os.path.exists(filename_data), msg
		except:
			raise ValueError(msg)
		narg   += 1


	# assert patterns:
	if data is None and filename_data is None:
		assert mode is None, 'If neither "data" nor "filename_data" are specified, "mode" cannot be specified.'
		assert filename_results is None, 'If neither "data" nor "filename_data" are specified, "filename_results" cannot be specified.'

	# launch app (Pattern 0): no arguments:
	path2app  = os.path.join( os.path.dirname(__file__) , 'ui', 'main.py')
	command   = 'python %s' %path2app

	# (Pattern 0): no arguments:
	if (data is None) and (filename_data is None):
		os.system(command)

	# (Pattern 1): data specified:
	else:
		if data is not None:
			fnameCSV    = os.path.join( os.getcwd(), '_temp_mwarp1d.csv' )
			np.savetxt(fnameCSV, data, delimiter=',')
			print('mwarp1d: temporary data file written to: %s.' %fnameCSV)
			
		else:
			fnameCSV = filename_data
		command     += ' %s' %fnameCSV
		
		if mode is not None:
			command += ' %s' %mode
		if filename_results is not None:
			command += ' %s' %filename_results

		os.system(command)




class MWarpResults(object):
	def __init__(self, fnameNPZ):
		self.J        = None
		self.Q        = None
		self.fnameNPZ = fnameNPZ
		self.mode     = None
		self.fname0   = None
		self.fname1   = None
		self.y        = None   #sources (original)
		self.yw       = None   #sources (warped)
		self.y0       = None   #template
		self._parse()
		
	def __repr__(self):
		s   = 'MWarpResults\n'
		s  += '----- Overview -------------\n'
		s  += '    mode           = %s\n' %self.mode
		s  += '    nsources       = %d\n' %self.J
		s  += '    nnodes         = %d\n' %self.Q
		s  += '----- 1D Data -------------\n'
		s  += '    sources        = (%d,%d) array\n' %self.y.shape
		s  += '    sources_warped = (%d,%d) array\n' %self.yw.shape
		s  += '    template       = (%d,) array\n' %self.y0.size
		return s
		
	def _parse(self):
		with np.load(self.fnameNPZ, allow_pickle=True) as Z:
			self.mode                 = str( Z['mode'] )
			self.fname0               = str( Z['filename0'] )
			self.fname1               = str( Z['filename1'] )
			self.y0                   = Z['ydata_template']
			self.y                    = Z['ydata_sources']
			self.yw                   = Z['ydata_sources_warped']
			
			self.J                    = self.y.shape[0]
			self.Q                    = self.y0.size

			if self.mode == 'landmark':
				pass
				# landmarks_template = Z['landmarks_template']
				# landmarks_sources  = Z['landmarks_sources']
				# landmark_labels    = [str(s) for s in Z['landmark_labels']]

			elif self.mode == 'manual':
				swparams = Z['seqwarps']
				swarps   = []
				for params in swparams:
					sw   = SequentialManualWarp()
					if params is not None:
						for p in params:
							amp,center,head,tail = p
							w = ManualWarp1D(self.Q)
							w.set_center(center)
							w.set_amp(amp)
							w.set_head(head)
							w.set_tail(tail)
							sw.append( w )
					swarps.append(sw)
				self.smwarps  = swarps

	
	def apply_warps(self, y):
		### presumes that the first row is the template
		return np.array([y[0]] + [ww.apply_warp_sequence(yy)   for ww,yy in zip(self.smwarps, y[1:])])
		


def loadnpz(fname):
	return MWarpResults(fname)
	

	
