import numpy as np
from scipy import optimize 
import multiprocessing as mp
from functools import partial
import csv

adB_BOUNDS = [1E-11 ,1E-6];
BETA_BOUNDS = [0.01, 0.7];


def calcSNR(g2Data):
	return np.abs((np.mean(g2Data, axis=0) - 1) / (np.std(g2Data, axis=0)));

def calcBeta(g2Data, limit=5):
	return np.mean(g2Data[1:limit]) -1;

def G1Calc(g2Data):
	beta = calcBeta(g2Data);
	g1Data = np.sqrt(np.abs((g2Data-1)/beta));
	return g1Data, beta;

def G1Analytical(alpha, tauList, rho=2, no=1.33, wavelength=8.48E-5, mua=0.1, musp=10):
	k0=2*np.pi*no/(wavelength);
	k=np.sqrt(3*mua*musp+6*musp*musp*k0*k0*alpha*tauList);
	n=no/1;
	Reff=-1.44/(n*n)+0.710/n+0.668+0.00636*n;
	zb=(2*(1+Reff))/(3*musp*(1-Reff));
	r1=np.sqrt(1/(musp*musp)+rho*rho);
	rb=np.sqrt((2*zb+1)**2/(musp*musp)+rho*rho);
	G1=np.exp(-k*r1)/r1-np.exp(-k*rb)/rb;
	G1_0=np.exp(-np.sqrt(3*mua*musp)*r1)/r1-np.exp(-np.sqrt(3*mua*musp)*rb)/rb;
	g1=G1/G1_0;
	return g1;

def G2Analytical(alpha, beta, tauList, rho=2, no=1.33, wavelength=8.48E-5, mua=0.1, musp=10):
	g1 = G1Analytical(alpha, tauList, rho, no, wavelength, mua, musp);
	return np.square(g1) * beta + 1;

def G1Fit(g1Data, tauList, SNR, p0=1E-8, rho=2, no=1.33, wavelength=8.48E-5, mua=0.1, musp=10):
	def f(tau, adB):
		return G1Analytical(adB, tau, rho, no, wavelength, mua, musp)*SNR;

	(params, params_covariance) = optimize.curve_fit(f, tauList, g1Data*SNR, p0, bounds=adB_BOUNDS);
	return params;

def G2Fit(g2Data, tauList, SNR, p0=[1E-8, 0.2], rho=2, no=1.33, wavelength=8.48E-5, mua=0.1, musp=10, ECC=False):
	def f(tau, adB, beta):
		return G2Analytical(adB, beta, tau, rho, no, wavelength, mua, musp)*SNR;

	try:
		(params, params_covariance) = optimize.curve_fit(f, tauList, g2Data*SNR, p0, bounds=((adB_BOUNDS[0], BETA_BOUNDS[0]), (adB_BOUNDS[1], BETA_BOUNDS[1])));
		return params;
	except:
		print("fit Error:");
		if(ECC):
			g1Data, beta = G1Calc(g2Data);
			flow = G1Fit(G1Data, tauList, SNR, rho=2, no=1.33, wavelength=8.48E-5, mua=0.1, musp=10);
			return flow, beta;
		# print(g2Data)
		# print(tauList)
		# print(SNR);
		return(0, 0);

def flowFitSingle(g2Data, tauList, rho=2, no=1.33, wavelength=8.48E-5, mua=0.1, musp=10, numProcessors=4):
	g2Data = g2Data[:, 1:];
	tauList = tauList[1:];

	SNR = calcSNR(g2Data);
	meanG2 = np.mean(g2Data, axis=0);
	meanG1 = G1Calc(g2Data);
	p0 = G1Fit(meanG1, tauList, SNR=SNR, rho=rho, no=no, wavelength=wavelength, mua=mua, musp=musp);

	pool = mp.Pool(processes=numProcessors);
	fcn = partial(G1Fit, tauList=tauList, SNR=SNR, p0=p0, rho=rho, no=no, wavelength=wavelength, mua=mua, musp=musp);

	g1Data = np.array(pool.map(G1Calc, g2Data));
	beta = g1Data[:, 1];
	g1Data = g1Data[:, 0];

	data = pool.map(fcn, g1Data);

	return data, beta;

def flowFitDual(g2Data, tauList, rho=2, no=1.33, wavelength=8.48E-5, mua=0.1, musp=10, numProcessors=4, ECC=False):
	g2Data = g2Data[:, 1:];
	tauList = tauList[1:];

	SNR = calcSNR(g2Data);
	meanG2 = np.mean(g2Data, axis=0);
	p0 = G2Fit(meanG2, tauList, SNR=SNR, rho=rho, no=no, wavelength=wavelength, mua=mua, musp=musp, ECC=ECC);


	pool = mp.Pool(processes=numProcessors);
	fcn = partial(G2Fit, tauList=tauList, SNR=SNR, p0=p0, rho=rho, no=no, wavelength=wavelength, mua=mua, musp=musp, ECC=ECC);

	data = np.array(pool.map(fcn, g2Data));

	return data[:, 0], data[:, 1];


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

	filenames = [path+'/G2Channel0', path+'/G2Channel1', path+'/G2Channel2', path+'/G2Channel3'];

	g2Data = pool.map(loadG2, filenames);

	tauList = [];
	with open(path+'/TAU', 'r') as tauFile:
		tauReader = csv.reader(tauFile, quoting=csv.QUOTE_NONNUMERIC);
		for row in tauReader:
			tauList.append(row);


	return np.array(g2Data), np.array(tauList)[0];


