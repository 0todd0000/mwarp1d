'''
Launch the mwarp1d GUI from IPython
'''

import mwarp1d
mwarp1d.launch_gui()



#Optional input arguments are shown below as comments
# See the following link for more details:
#    http://www.spm1d.org/mwarp1d/manual/commandline.html


# launch_gui( fnameNPZ ) #resume previous session using an existing mwarp1d results file
# launch_gui( fnameCSV ) #launch new session using data from CSV file
# launch_gui( fnameCSV , mode ) #launch new session with CSV data in specified mode
# launch_gui( fnameCSV , mode , fnameNPZ ) #launch new session with CSV data in specified mode, with results saved to fnameNPZ


