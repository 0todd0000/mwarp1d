
import numpy as np

from . import DataLandmarks,DataManual

def loadnpz(fname):
	with np.load(fname) as Z:
		mode                   = str( Z['mode'] )
		fname0                 = str( Z['filename0'] )
		fname1                 = str( Z['filename1'] )
		ydata_template         = Z['ydata_template']
		ydata_sources          = Z['ydata_sources']
		ydata_sources_warped   = Z['ydata_sources_warped']
	
		if mode == 'landmarks':
			landmarks_template = Z['landmarks_template']
			landmarks_sources  = Z['landmarks_sources']
			landmark_labels    = [str(s) for s in Z['landmark_labels']]

	data = DataManual() if (mode == 'manual') else DataLandmarks()
	data.set_input_filename(fname0, read=False)
	data.set_output_filename(fname)
	data.set_template( ydata_template )
	data.set_sources( ydata_sources, init_warped=False )
	data.set_sources_warped( ydata_sources_warped )

	if mode == 'landmarks':
		data.set_landmark_labels( landmark_labels )
		data.set_template_landmarks( landmarks_template )
		data.set_source_landmarks( landmarks_sources )

	return data


