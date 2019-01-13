import numpy as np

class G1Converter:
	def calcBeta(g2Data, limit=5):
		return np.mean(g2Data[1:limit]);

	def G1Calc(g2Data):
		beta = calcBeta(g2Data);
		g1Data = np.sqrt(np.abs((g2Data-1)/beta));