import numpy as np

class G1Converter:
	def calcBeta(g2Data, limit=5):
		return np.mean(g2Data[1:limit, 1]);

	def G1Calc(g2Data)
