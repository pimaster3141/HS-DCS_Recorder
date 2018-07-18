import G2Calc
import csv
import os
import numpy as np

def ultimateCruncher(filename, fs=10E6, intg=0.1, fs_out=200):
	f = open(filename, 'rb');
	fsize = os.stat(filename).st_size;
	byteCounter = 0;
	currentCounter = 0;
	lastByte = 0;

	cruncher = G2Calc.MTau(fs, int(fs*intg), int(fs/fs_out));
	output = []
	vaporizer = np.array([], dtype=np.uint8)
	taus = np.array([])
	while(byteCounter < fsize):
		data = f.read(10240000);
		if(data == ''):
			break;
		byteCounter = byteCounter + len(data);
		currentCounter = currentCounter + len(data);

		#data = data[::2];

		data = np.frombuffer(data, dtype=np.int8);
		vap = data < 0;
		data = data + vap*128;
		vap = np.array(vap[::int(fs/fs_out)], dtype=np.uint8);
		vaporizer = np.append(vaporizer, vap*1);

		data = np.append(lastByte, data);
		lastbyte = data[-1];
		data = np.diff(data);
		e = data<0;
		data = data+ e*16;


		temp = cruncher.update(data);
		for i in temp:
			taus = i[:,0];
			output.append(i[:,1]);

		if(currentCounter > int(fsize/100)):
			percentage = int(100*byteCounter/fsize);
			print("%d%% Done" % percentage);
			currentCounter = 0;

		#print(len(vap));
		#print(len(temp));


	vaporizer = np.array(vaporizer, dtype=np.uint8);
	print(len(vaporizer));
	print(len(output));
	return (output, taus, vaporizer);

def outWrite(filename, g2, tau, vap):
	with open(filename+"_G2", 'w', newline='') as g2File:
		g2writer = csv.writer(g2File);
		for g in g2:
			g2writer.writerow(g);

	with open(filename+"_tau", 'w', newline='') as tauFile:
		tauwriter = csv.writer(tauFile);
		tauwriter.writerow(tau);

	with open(filename+"_vap", 'wb') as vapFile:
		vapFile.write(bytes(vap));

def runner(filename, fs, intg=0.1):
	print("Processing Files");
	(g, t, v) = ultimateCruncher(filename, fs, intg);
	print("creating Files");
	outWrite(filename, g, t, v);
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

