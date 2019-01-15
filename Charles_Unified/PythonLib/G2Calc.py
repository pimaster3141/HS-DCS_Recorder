import multipletau as mt
import numpy as np

def mtAuto(data, fs=10E6, levels=16):
	out = mt.autocorrelate(data, m=levels, deltat=1.0/fs, normalize=True);
	out[:,1] = out[:,1]+1;
	return out;