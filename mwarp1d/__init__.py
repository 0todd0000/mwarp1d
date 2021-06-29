
'''
mwarp1d:  Manual one-dimensional data warping and nonlinear registration in Python and PyQt

Copyright (C) 2021  Todd Pataky
Version: 0.2.2 (2021-06-29)
'''


__version__ = '0.2.2'  #2021-06-29

from . manual import *
from . landmark import *
from . uii import *


def get_data_dir():
	import os
	dir_root     = os.path.dirname( __file__ )
	dir_data     = os.path.join( dir_root , 'examples', 'data' )
	return dir_data
