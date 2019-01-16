import sys
sys.path.insert(0, 'PythonLib');

import FlowFit
import G2Calc
import HSDCSParser
import G2Extract
import multiprocessing as mp
import csv
import numpy as np
from functools import partial
import os
import time

def extractG2(filename, legacy=False, fs=2.5E6, intg=0.05, fsout=200, numProcessors=6):
	(g, t, v) = G2Extract.calculateG2(filename, legacy, fs, intg, fsout, numProcessors);
	G2Extract.writeG2Data(filename, g, t, v, legacy, fs, intg, fsout);
	print("Completed G2");

def legacyExtract(folder, averages, fs=2.5E6, rho=2, no=1.33, wavelength=8.48E-5, mua=0.1, musp=10, numProcessors=6, ssd=True):
	print("Loading Data");
	g2Data, tauList = loadLegacy(folder, ssd);
	for i in range(len(averages)):
		print("Fitting Channel: " + str(i));
		average = averages[i];
		g2Avg = np.mean(g2Data[average[0]:average[1]+1], axis=0);
		flow, beta = FlowFit.flowFitDual(g2Avg, tauList, rho, no, wavelength, mua, musp, numProcessors, chunksize=200, ECC=False);
		count = fs/g2Avg[:, 0];
		flowWriter(folder, average, flow, beta, count, fs, rho, no, wavelength, mua, musp);

	with open(folder + "/INFO", 'w', newline='') as countFile:
		countFile.write("fs=" + str(fs) + "\n");
		countFile.write("averages=" + str(averages) + "\n");
		countFile.write("rho=" + str(rho) + "\n");
		countFile.write("no=" + str(no) + "\n");
		countFile.write("wavelength=" + str(wavelength) + "\n");
		countFile.write("mua=" + str(mua) + "\n");
		countFile.write("musp=" + str(musp) + "\n");

def batchLegacyExtract(directory, folderList, averages, fs=2.5E6, rho=2, no=1.33, wavelength=8.48E-5, mua=0.1, musp=10, numProcessors=6, ssd=True):
	for folder in folderList:
		print("File: " +directory+folder);
		path = directory+folder;
		legacyExtract(path, averages, fs=2.5E6, rho=2, no=1.33, wavelength=8.48E-5, mua=0.1, musp=10, numProcessors=6, ssd=True);



