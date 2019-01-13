import numpy as np
from scipy import optimize 



def calcBeta(g2Data, limit=5):
	return np.mean(g2Data[1:limit]) -1;

def G1Calc(g2Data):
	beta = calcBeta(g2Data);
	g1Data = np.sqrt(np.abs((g2Data-1)/beta));
	return g1Data;

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

def G1Fit(g1Data, tauList, SNR, rho=2, no=1.33, wavelength=8.48E-5, mua=0.1, musp=10):
	def f(x, adB):
		return G1Analytical(adB, x, rho=2, no=1.33, wavelength=8.48E-5, mua=0.1, musp=10)*SNR;

	
	(params, params_covariance) = optimize.curve_fit(f, tauList, g1Data*SNR, p0=1E-8, bounds=(1E-10, 1E-7));
	return params;

def flowFit

