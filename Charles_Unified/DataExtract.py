import sys
sys.path.insert(0, 'PythonLib');

import FlowExtract
import G2Extract

def extractG2(filename, legacy=False, fs=2.5E6, intg=0.05, fsout=200, numProcessors=6):
	print("Extracting: " + filename);
	(g, t, v) = G2Extract.calculateG2(filename, legacy, fs, intg, fsout, numProcessors);
	folder = G2Extract.createFolder(filename, intg);
	G2Extract.writeG2Data(folder, g, t, v, legacy, fs, intg, fsout);
	print("Completed G2");

def extractFlow(folder, averages, fs=2.5E6, rho=2, no=1.33, wavelength=8.48E-5, mua=0.1, musp=10, numProcessors=6):
	print("Extracting: " + folder);
	(g, t, v) = G2Extract.loadG2(folder);
	(flows, betas, counts) = FlowExtract.calculateFlow(g, t, averages, fs, rho, no, wavelength, mua, musp, numProcessors);
	FlowExtract.writeFlowData(folder, flows, betas, counts, averages, rho, no, wavelength, mua, musp);
	print("Completed Flow");

def batchExtractFlow(folders, averages,fs=2.5E6, rho=2, no=1.33, wavelength=8.48E-5, mua=0.1, musp=10, numProcessors=6):
	for f in folders:
		extractFlow(f, averages, fs, rho, no, wavelength, mua, musp, numProcessors);

def fullExtract(filename, averages, legacy=False, fs=2.5E6, intg=0.05, fsout=200, rho=2, no=1.33, wavelength=8.48E-5, mua=0.1, musp=10, numProcessors=6):
	print("Extracting: " + filename);
	(g, t, v) = G2Extract.calculateG2(filename, legacy, fs, intg, fsout, numProcessors);
	folder = G2Extract.createFolder(filename, intg);
	G2Extract.writeG2Data(folder, g, t, v, legacy, fs, intg, fsout);
	print("Completed G2");
	(flows, betas, counts) = FlowExtract.calculateFlow(g, t, averages, fs, rho, no, wavelength, mua, musp, numProcessors);
	FlowExtract.writeFlowData(folder, flows, betas, counts, averages, rho, no, wavelength, mua, musp);
	print("Completed Flow");

def batchFullExtract(files, averages, legacy=False, fs=2.5E6, intg=0.05, fsout=200, rho=2, no=1.33, wavelength=8.48E-5, mua=0.1, musp=10, numProcessors=6):
	for f in files:
		fullExtract(f, averages, legacy, fs, intg, fsout, rho, no, wavelength, mua, musp, numProcessors)
# def batchLegacyExtract(directory, folderList, averages, fs=2.5E6, rho=2, no=1.33, wavelength=8.48E-5, mua=0.1, musp=10, numProcessors=6, ssd=True):
# 	for folder in folderList:
# 		print("File: " +directory+folder);
# 		path = directory+folder;
# 		legacyExtract(path, averages, fs=2.5E6, rho=2, no=1.33, wavelength=8.48E-5, mua=0.1, musp=10, numProcessors=6, ssd=True);



