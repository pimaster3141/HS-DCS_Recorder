import multipletau as mt
import numpy as np

import warnings

def mtAuto(data, fs=10E6, levels=16):
	with warnings.catch_warnings():
		warnings.simplefilter("ignore");
		try:
			out = mt.autocorrelate(data, m=levels, deltat=1.0/fs, normalize=True);
		except:
			data[0] = 1;
			out = mt.autocorrelate(data, m=levels, deltat=1.0/fs, normalize=True);
		out[:,1] = out[:,1]+1;
		return out;

def mtAutoQuad(data, fs=2.5E6, levels=16):
	g20 = mtAuto(data[0,:], fs, levels)[:,1];
	g21 = mtAuto(data[1,:], fs, levels)[:,1];
	g22 = mtAuto(data[2,:], fs, levels)[:,1];
	g23 = mtAuto(data[3,:], fs, levels)[:,1];

	return np.array((g20, g21, g22, g23));
