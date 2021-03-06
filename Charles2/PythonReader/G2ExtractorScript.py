import G2Calc
import DCSReader
import csv
import os
import numpy as np
import math
import code

BYTES_PER_SAMPLE = 2;

def ultimateCruncher(filename, fs=2E6, intg=0.1, fs_out=100):
	f = open(filename, 'rb');
	fsize = os.stat(filename).st_size;

	windowSize = int(fs*intg);
	windowShift = int(fs/fs_out);
	numSamples = math.floor(((fsize/BYTES_PER_SAMPLE)-windowSize)/windowShift)+1;
	currentCounter = 0;
	print(numSamples);

	initData = f.read(windowSize*BYTES_PER_SAMPLE);
	(photon, vap) = DCSReader.extractSignals(initData);

	channelCrunchers = [];
	g2 = []
	markers = []
	tauList = None;
	for c in range(4):
		channelCrunchers.append(G2Calc.MTau(fs, photon[c]));
		initG2 = channelCrunchers[c].getInitial();
		tauList = initG2[:,0];

		g2.append(np.zeros([numSamples, len(tauList)]));
		g2[c][0] = initG2[:,1];

		markers.append(np.zeros([numSamples, 1], dtype=np.uint8));
		markers[c][0] = np.sum(vap[c]) != 0;

	loopCounter = 0;
	while(currentCounter < numSamples-1):
		currentCounter = currentCounter + 1;
		data = f.read(windowShift*BYTES_PER_SAMPLE);
		
		if(len(data) < windowShift*BYTES_PER_SAMPLE):
			break;

		(photon, vap) = DCSReader.extractSignals(data);

		for c in range(4):
			currentG2 = channelCrunchers[c].update(photon[c]);
			g2[c][currentCounter] = currentG2;

			markers[c][currentCounter] = np.sum(vap[c]) != 0;

		loopCounter = loopCounter + 1;
		if(loopCounter > numSamples/100):
			percentage = int(100*currentCounter/numSamples);
			print("%d%% Done" % percentage);
			loopCounter = 0;

	return (g2, tauList, markers);

def outWrite(filename, g2, tau, vap, intg, fs_out):
	BW = int(1.0/intg + 0.5);

	if not os.path.exists(filename + str(BW) +"Hz/"):
		os.makedirs(filename + str(BW) +"Hz/")

	for c in range(4):
		with open(filename + str(BW) +"Hz/G2channel"+str(c), 'w', newline='') as g2File:
			g2writer = csv.writer(g2File);
			for g in g2[c]:
				g2writer.writerow(g);

		with open(filename + str(BW) +"Hz/VAPchannel"+str(c), 'wb') as vapFile:
			vapFile.write(bytes(vap[c]));

	with open(filename + str(BW) +"Hz/TAU", 'w', newline='') as tauFile:
		tauwriter = csv.writer(tauFile);
		tauwriter.writerow(tau);

def runner(filename, fs, intg=0.1, fsout=100):
	print("Processing Files");
	(g, t, v) = ultimateCruncher(filename, fs, intg, fsout);
	print("creating Files");
	outWrite(filename, g, t, v, intg, fsout);
	print("done");



#runner('Finger_10MHz', 10E6);
#runner('Finger2_10MHz', 10E6, intg=0.05);
#runner('Head(Jana)_2MHz', 2E6);
#runner('Head_10MHz', 10E6);
#runner('Milk_10MHz', 10E6);
#runner('arm_2MHz', 2E6, intg=0.05);
#runner('Head2_2MHz', 2E6);
#runner('Head2_Copy', 2E6, intg=0.05);

##runner('test-30kcps', fs=2E6, intg=0.1);
##runner('test-30kcps-2', fs=2E6, intg=0.1);
##runner('test-50kcps', fs=2E6, intg=0.1);
##runner('test-50kcps-2', fs=2E6, intg=0.1);
##runner('test-80kcps', fs=2E6, intg=0.1);
##runner('test-80kcps-2', fs=2E6, intg=0.1);
##runner('test-80kcps-3', fs=2E6, intg=0.1);
##runner ('test-30kcps-2_lowINT', fs=2E6, intg=0.05);
code.interact(local = locals());
