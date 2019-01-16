import sys
sys.path.insert(0, 'PythonLib');

import FlowFit
import G2Calc
import HSDCSParser
import multiprocessing as mp
import csv
import numpy as np
from functools import partial
import os
import time

BYTES_PER_SAMPLE = 2;
SAMPLE_DTYPE = 'int16';

def extractG2(filename, legacy=False, fs=2.5E6, intg=0.05, fsout=200, numProcessors=12):
	start = time.time();
	fsize = os.stat(filename).st_size;
	windowSize = int(fs*intg);
	windowShift = int(fs/fsout);
	numSamples = np.floor(((fsize/BYTES_PER_SAMPLE)-windowSize)/windowShift)+1;

	tauList = G2Calc.mtAuto(np.ones(windowSize), fs=fs, levels=16)[:,0];

	startIndexes = np.arange(numSamples, dtype='uint8')*windowShift;
	pool = mp.Pool(processes=numProcessors);
	fcn = partial(seekExtract, windowSize=windowSize, fs=fs, levels=16, legacy=False, filename=filename);

	data = pool.map(fcn, startIndexes, chunksize=100);

	pool.close();
	pool.join();

	g2Data = [item[0] for item in data];
	count = [item[1] for item in data];
	vap = [item[2] for item in data];
	print(time.time()-start);
	return (g2Data, tauList, vap, count);

def seekExtract(startIndex, windowSize, fs, levels, legacy, filename):
	f = open(filename, 'rb');
	f.seek(startIndex*BYTES_PER_SAMPLE, os.SEEK_SET);
	data = np.fromfile(f, count=windowSize, dtype=SAMPLE_DTYPE);

	channel, vap = HSDCSParser.parseCharles2(data);

	g2Data = G2Calc.mtAutoQuad(channel, fs, levels);
	count = fs/g2Data[:,0];
	vap = np.array((np.mean(vap, axis=1)+.5), dtype=np.int8);

	return (g2Data, count, vap)

def loadG2(filename):
	g2Data = [];
	with open(filename, 'r') as g2File:
		g2Reader = csv.reader(g2File, quoting=csv.QUOTE_NONNUMERIC);
		for row in g2Reader:
			g2Data.append(row);

	g2Data = np.array(g2Data);
	return g2Data;

def loadLegacy(path, ssd=True):
	pool = mp.Pool(processes=1);
	if(ssd):
		pool = mp.Pool(processes=4);

	filenames = [path+'/G2channel0', path+'/G2channel1', path+'/G2channel2', path+'/G2channel3'];

	g2Data = pool.map(loadG2, filenames);

	pool.close();
	pool.join();

	tauList = [];
	with open(path+'/TAU', 'r') as tauFile:
		tauReader = csv.reader(tauFile, quoting=csv.QUOTE_NONNUMERIC);
		for row in tauReader:
			tauList.append(row);

	return np.array(g2Data), np.array(tauList)[0];

def legacyExtract(folder, averages, fs=2.5E6, rho=2, no=1.33, wavelength=8.48E-5, mua=0.1, musp=10, numProcessors=12, ssd=True):
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

def batchLegacyExtract(directory, folderList, averages, fs=2.5E6, rho=2, no=1.33, wavelength=8.48E-5, mua=0.1, musp=10, numProcessors=12, ssd=True):
	for folder in folderList:
		print("File: " +directory+folder);
		path = directory+folder;
		legacyExtract(path, averages, fs=2.5E6, rho=2, no=1.33, wavelength=8.48E-5, mua=0.1, musp=10, numProcessors=12, ssd=True);



