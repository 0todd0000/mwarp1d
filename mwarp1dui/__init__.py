


import sys,os



# path2app     = '/Users/todd/Dropbox/2019Sync/Documents/Projects/projects/inlreg1d/Python/ui/main.py'
# os.system( path2app )
#
#
# # mode         = 'landmarks'
# # # mode         = 'manual'
# # # fnameCSV     = '/Users/todd/Dropbox/2019Sync/Documents/Projects/projects/inlreg1d/Data/Case3/sources.csv'
# # fnameCSV     = '/Users/todd/Dropbox/2019Sync/Documents/Projects/projects/inlreg1d/Data/1000/sources.csv'
# # fnameNPZ     = '/Users/todd/Desktop/results.npz'
# # # # fnameNPZ     = dir0 + 'results.npz'
# # fnameNPZ     = '/Users/todd/Desktop/results.npz'
# #
# #
# # command     = 'python %s %s %s %s' %(path2app, mode, fnameCSV, fnameNPZ)
# #
# # os.system( command )



def launch_gui(*args):
	from . main import MainApplication
	print(MainApplication)
	
	#
	# app    = MainApplication(sys.argv)
	# app.setApplicationName("mwarp1d")
	# window = MainWindow( sys.argv )
	# window.move(0, 0)
	# window.show()
	# sys.exit(app.exec_())

