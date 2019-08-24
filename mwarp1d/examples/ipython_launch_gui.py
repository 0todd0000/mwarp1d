'''
Launch the mwarp1d GUI from IPython

Optional arguments to the mwarp1d.launch_gui function include:

* data            #2D numpy array
* filename_data   #csv file name containing input data
* mode   #'landmark' or 'manual'
* filename_results  #npz file name into which warp session data will be saved

The following patterns are acceptable:

mwarp1d.launch_gui(data)
mwarp1d.launch_gui(data, mode)
mwarp1d.launch_gui(data, mode, filename_results)

mwarp1d.launch_gui(filename_data)
mwarp1d.launch_gui(filename_data, mode)
mwarp1d.launch_gui(filename_data, mode, filename_results)

mwarp1d.launch_gui(filename_results='/Users/username/results.npz')

'''

import mwarp1d



#(Pattern 0): No input arguments
mwarp1d.launch_gui()



# #(Pattern 1): CSV data specified:
# fnameCSV = '/Users/todd/GitHub/mwarp1d/examples/data/Dorn2012-1000nodes.csv'
# mwarp1d.launch_gui(fnameCSV)


# #(Pattern 1a): other options
# mwarp1d.launch_gui(y, mode='landmarks')


# #(Pattern 2): numpy data specified:
# fnameCSV = '/Users/todd/GitHub/mwarp1d/examples/data/Dorn2012-1000nodes.csv'
# y        = np.loadtxt(fnameCSV, delimiter=',')
# mwarp1d.launch_gui(y)
