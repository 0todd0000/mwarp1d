
from setuptools import setup



long_description = '''
Manual one-dimensional data warping and nonlinear registration in Python and PyQt.
'''

setup(
	name             = 'mwarp1d',
	version          = '0.0.2',
	description      = 'Manual warping for one-dimensional data',
	author           = 'Todd Pataky',
	author_email     = 'spm1d.mail@gmail.com',
	url              = 'https://github.com/0todd0000/mwarp1d',
	download_url     = 'https://github.com/0todd0000/mwarp1d/archive/master.zip',
	packages         = ['mwarp1d'],
	package_data     = {'mwarp1d' : ['examples/*.*', 'ui/*.*'] },
	include_package_data = True,
	long_description = long_description,
	keywords         = ['statistics', 'time series analysis'],
	classifiers      = [],
	install_requires = ["future", "numpy", "scipy", "matplotlib"]
) 