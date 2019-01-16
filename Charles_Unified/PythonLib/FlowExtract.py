import FlowFit
import numpy as np
import time

def calculateFlow(g2Data, tauList, averages, fs=2.5E6, rho=2, no=1.33, wavelength=8.48E-5, mua=0.1, musp=10, numProcessors=6):
	start = time.time();
	flows = [];
	betas = [];
	for i in range(len(averages)):
		print("Fitting Channel Average: " + str(averages[i]));
		average = averages[i];
		g2Avg = np.mean(g2Data[average[0]:average[1]+1], axis=0);
		flow, beta = FlowFit.flowFitDual(g2Avg, tauList, rho, no, wavelength, mua, musp, numProcessors, chunksize=200, ECC=False);
		count = fs/g2Avg[:, 0];


def writeFlowData(folder, average, flow, beta, count, fs, rho, no, wavelength, mua, musp):
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

def writeNotes(folder, averages, rho, no, wavelength, mua, msp):
	print("Writing Flow Notes");
	with open(folder + "/INFO", 'w', newline='') as countFile:
		countFile.write("fs=" + str(fs) + "\n");
		countFile.write("averages=" + str(averages) + "\n");
		countFile.write("rho=" + str(rho) + "\n");
		countFile.write("no=" + str(no) + "\n");
		countFile.write("wavelength=" + str(wavelength) + "\n");
		countFile.write("mua=" + str(mua) + "\n");
		countFile.write("musp=" + str(musp) + "\n");