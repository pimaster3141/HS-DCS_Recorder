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

BYTES_PER_SAMPLE = 2;
SAMPLE_DTYPE = 'int16';

def extractG2(filename, legacy=False, fs=2.5E6, intg=0.05, fsout=200, numProcessors=6):
	(g, t, v) = G2Extract.calculateG2(filename, legacy, fs, intg, fsout, numProcessors);
	print("Creating Files");
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

def flowWriter(folder, average, flow, beta, count, fs, rho, no, wavelength, mua, musp):
	print("Writing Files");
	with open(folder + "/flow" + str(average[0]) + str(average[1]), 'w', newline='') as flowFile:
		flowWriter = csv.writer(flowFile);
		flowWriter.writerow(flow);

	with open(folder + "/beta" + str(average[0]) + str(average[1]), 'w', newline='') as betaFile:
		betaWriter = csv.writer(betaFile);
		betaWriter.writerow(beta);

	with open(folder + "/count" + str(average[0]) + str(average[1]), 'w', newline='') as countFile:
		countWriter = csv.writer(countFile);
		countWriter.writerow(count);
	return;

def batchLegacyExtract(directory, folderList, averages, fs=2.5E6, rho=2, no=1.33, wavelength=8.48E-5, mua=0.1, musp=10, numProcessors=6, ssd=True):
	for folder in folderList:
		print("File: " +directory+folder);
		path = directory+folder;
		legacyExtract(path, averages, fs=2.5E6, rho=2, no=1.33, wavelength=8.48E-5, mua=0.1, musp=10, numProcessors=6, ssd=True);



