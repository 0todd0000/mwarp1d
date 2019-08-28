
'''
Functions and classes for interfacing with the UI via scripting
'''

import numpy as np
from . manual import ManualWarp1D, SequentialManualWarp
from . landmark import warp_landmark



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
			self.mode              = str( Z['mode'] )
			self.fname0            = str( Z['filename0'] )
			self.fname1            = str( Z['filename1'] )
			self.y0                = Z['ydata_template']
			self.y                 = Z['ydata_sources']
			self.yw                = Z['ydata_sources_warped']
			
			self.J                 = self.y.shape[0]
			self.Q                 = self.y0.size

			if self.mode == 'landmark':
				landmarks_template = Z['landmarks_template']
				landmarks_sources  = Z['landmarks_sources']
				landmark_labels    = [str(s) for s in Z['landmark_labels']]
				self.lm0           = landmarks_template
				self.lm            = landmarks_sources

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

	
	@property
	def nnodes(self):
		return self.Q
	@property
	def nsources(self):
		return self.J
	@property
	def sources(self):
		return self.y
	@property
	def sources_warped(self):
		return self.yw
	@property
	def template(self):
		return self.y0
	
	
	def apply_warps(self, y):
		assert isinstance(y, np.ndarray), 'y must be a numpy array'
		assert y.ndim==2, 'y must be a 2D numpy array'
		J,Q = y.shape
		assert (J==self.J) or (J==(self.J+1)), 'y must have %d rows (if y contains only sources) or %d rows (if y contains both template and sources)' %(self.J, self.J+1)
		assert Q==self.Q, 'y must have %d columns' %self.Q
		
		if self.mode=='manual':
			if J==self.J: #only sources submitted
				yw = [ww.apply_warp_sequence(yy)   for ww,yy in zip(self.smwarps, y)]
			else: #template also submitted (first row)
				yw = [ww.apply_warp_sequence(yy)   for ww,yy in zip(self.smwarps, y[1:])]
				yw = [y[0]] + yw
				
		elif self.mode=='landmark':
			if J==self.J: #only sources submitted
				yw = [warp_landmark(yy, lm, self.lm0)  for lm,yy in zip(self.lm,y)]
			else: #template also submitted (first row)
				yw = [warp_landmark(yy, lm, self.lm0)  for lm,yy in zip(self.lm,y[1:])]
				yw = [y[0]] + yw
			
		return np.array(yw)





def launch_gui(*args):
	'''
	Command-line access to GUI launching.
	
	This function allows the user to bypass the initial GUI screen and proceed
	directly to the specified warping interface, thereby avoiding manual GUI setup.
	It also allows you to resume previous mwarp1d sessions.
	
	This function can be called from both Python and interactive Python. The GUI will
	be launched as a subprocess of the active Python kernel.
	
	:Args:
		
		**data** --- a 2D numpy array (rows = observations, columns = domain nodes)
		
		**fnameCSV** --- CSV file name containing a 2D array (rows = observations, columns = domain nodes)
		
		**fnameNPZ** --- NPZ file name (zipped numpy format) containing mwarp1d results (existing or to be written)

		**mode** --- "landmark" or "manual"
	
	:Arg options:
	
		* launch_gui()                              #launch new session with no data
		
		* launch_gui( fnameNPZ )                    #resume previous session using an existing mwarp1d results file
		
		* launch_gui( fnameCSV )                    #launch new session using data from CSV file
		
		* launch_gui( fnameCSV , mode )             #launch new session with CSV data in specified mode
		
		* launch_gui( fnameCSV , mode , fnameNPZ )  #launch new session with CSV data in specified mode, with results saved to fnameNPZ
	'''
	import os
	narg          = len(args)
	path2app      = os.path.join( os.path.dirname(__file__) , 'ui', 'main.py')
	
	
	if narg == 0:
		command   = 'python %s' %path2app

		
	elif narg == 1:
		fname     = args[0]
		assert isinstance(fname, str), 'Input argument must be a file name'
		assert os.path.exists(fname), 'File does not exist. (%s)' %fname
		ext       = os.path.splitext(fname)[1][1:].upper()
		assert ext in ['CSV', 'NPZ'], 'File extension must be .csv or .npz'
		#build command
		command   = 'python %s %s' %(path2app, fname)


	elif narg == 2:
		fnameCSV  = args[0]
		mode      = args[1]
		#check fnameCSV
		assert isinstance(fnameCSV, str), 'First input argument must be a file name'
		assert os.path.exists(fnameCSV), 'File does not exist. (%s)' %fnameCSV
		ext       = os.path.splitext(fnameCSV)[1][1:].upper()
		assert ext == 'CSV', 'File extension must be .csv'
		#check mode
		assert isinstance(mode, str), 'Second argument must be "landmark" or "manual"'
		assert mode in ['landmark','manual'], 'Second argument must be "landmark" or "manual"'
		#build command
		command   = 'python %s %s %s' %(path2app, fnameCSV, mode)

		
	elif narg == 3:
		fnameCSV  = args[0]
		mode      = args[1]
		fnameNPZ  = args[2]
		#check fnameCSV
		assert isinstance(fnameCSV, str), 'First input argument must be a file name'
		assert os.path.exists(fnameCSV), 'File does not exist. (%s)' %fname
		ext       = os.path.splitext(fnameCSV)[1][1:].upper()
		assert ext == 'CSV', 'First argument must be a file name with extension .csv'
		#check mode
		assert isinstance(mode, str), 'Second argument must be "landmark" or "manual"'
		assert mode in ['landmark','manual'], 'Second argument must be "landmark" or "manual"'
		command   = 'python %s %s %s' %(path2app, fnameCSV, mode)
		#check fnameNPZ
		assert isinstance(fnameNPZ, str), 'Third input argument must be a file name'
		ext       = os.path.splitext(fnameNPZ)[1][1:].upper()
		assert ext == 'NPZ', 'Third argument must be a file name with extension .npz'
		#build command
		command   = 'python %s %s %s %s' %(path2app, fnameCSV, mode, fnameNPZ)
		
		
	else:
		raise ValueError('Maximum three input arguments.')
	
	
	os.system(command)







def loadnpz(fname):
	'''
	Load mwarp1d compressed numpy (NPZ) file for results parsing.
	
	:Args:
	
		**fname** --- the NPZ file name
	
	:Example:
		>>> import numpy as np
		>>> from matplotlib import pyplot as plt
		>>>
		>>> with np.load(fnameNPZ) as Z:
		>>> 	print( Z['mode'] )
		>>> 	print( Z['ydata_template'].shape )
		>>> 	print( Z['ydata_sources'].shape )
		>>> 	print( Z['ydata_sources_warped'].shape )
		>>> 	
		>>> 	y = Z['ydata_sources']
		>>>
		>>> plt.figure()
		>>> plt.plot( y.T )
		>>> plt.show()
	
	
	:See also:
	
		 :ref:`Parsing GUI results <Parsing GUI results>`
	'''
	return MWarpResults(fname)
	

	
