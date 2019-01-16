import FlowFit
import numpy as np
import time
import csv


def calculateFlow(g2Data, tauList, averages, fs=2.5E6, rho=2, no=1.33, wavelength=8.48E-5, mua=0.1, musp=10, numProcessors=6):
	start = time.time();
	flows = [];
	betas = [];
	counts = [];
	for i in range(len(averages)):
		print("Fitting Channel Average: " + str(averages[i]));
		average = averages[i];
		g2Avg = np.mean(g2Data[average[0]:average[1]+1], axis=0);
		flow, beta = FlowFit.flowFitDual(g2Avg, tauList, rho, no, wavelength, mua, musp, numProcessors, chunksize=200, ECC=False);
		count = fs/g2Avg[:, 0];

		flows.append(flow);
		betas.append(beta);
		counts.append(count);

	print("Fit Computation time: " + str(time.time()-start));
	return np.array(flows), np.array(betas), np.array(counts);

def loadFlow(path):
	flow = loadFlowChannel(path+'/flow');
	beta = loadBetaChannel(path+'/beta');
	count = loadCountChannel(path+'/count');

	return (flow, beta, count)

def loadFlowChannel(filename):
	flowData = [];
	with open(filename, 'r') as flowFile:
		flowReader = csv.reader(flowFile, quoting=csv.QUOTE_NONNUMERIC);
		for row in flowReader:
			flowData.append(row);

	flowData = np.array(flowData);
	return flowData;

def loadBetaChannel(filename):
	betaData = [];
	with open(filename, 'r') as betaFile:
		betaReader = csv.reader(betaFile, quoting=csv.QUOTE_NONNUMERIC);
		for row in betaReader:
			betaData.append(row);

	betaData = np.array(betaData);
	return betaData;

def loadCountChannel(filename):
	countData = [];
	with open(filename, 'r') as countFile:
		countReader = csv.reader(countFile, quoting=csv.QUOTE_NONNUMERIC);
		for row in countReader:
			countData.append(row);

	countData = np.array(countData);
	return countData;

def writeFlowData(folder, flow, beta, count, averages, rho, no, wavelength, mua, musp):
	print("Writing Files");
	with open(folder + "/flow", 'w', newline='') as flowFile:
		flowWriter = csv.writer(flowFile);
		for f in flow:
			flowWriter.writerow(f);

	with open(folder + "/beta", 'w', newline='') as betaFile:
		betaWriter = csv.writer(betaFile);
		for b in beta:
			betaWriter.writerow(b);

	with open(folder + "/count", 'w', newline='') as countFile:
		countWriter = csv.writer(countFile);
		for c in count:
			countWriter.writerow(c);

	writeNotes(folder, averages, rho, no, wavelength, mua, musp);
	return;

def writeNotes(folder, averages, rho, no, wavelength, mua, musp):
	print("Writing Flow Notes");
	with open(folder + "/Flow_Parameters.txt", 'w', newline='') as countFile:
		countFile.write("averages=" + str(averages) + "\n");
		countFile.write("rho=" + str(rho) + "\n");
		countFile.write("no=" + str(no) + "\n");
		countFile.write("wavelength=" + str(wavelength) + "\n");
		countFile.write("mua=" + str(mua) + "\n");
		countFile.write("musp=" + str(musp) + "\n");