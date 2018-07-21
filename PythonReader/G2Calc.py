import multipletau as mt
import numpy as np

class MTau():
	def __init__(self, fs, initData):
		self._fs = fs;

		self.lastData = initData;

		return;


	def update(self, data):
		if(len(data) < len(self.lastData)):
			self.lastData = np.concatenate([self.lastData[len(data):], data]);
		else:
			self.lastData = data[(-1*len(self.lastData)):];
		try:
			output = mtAuto(self.lastData, fs=self._fs);
		except Exception as e:
			print(e);
			output = mtAuto(self.lastData + .001, fs=self._fs);
		return output[:,1];

	def getInitial(self):
		return mtAuto(self.lastData, fs=self._fs);




# class linear():

# 	def __init__(self, windowSize, numPoints=256):
# 		self._windowSize = windowSize;
# 		self._numPoints = numPoints;

# 		self.tauListN = np.logspace(0, np.log10(self._windowSize), self._numPoints, dtype='uint');
# 		self.tauListN = np.unique(self.tauListN);
# 		self.currData = np.zeros(self._windowSize, 'uint8');

# 	def 

def mtAuto(data, fs=10E6, levels=16):
	out = mt.autocorrelate(data, m=levels, deltat=1.0/fs, normalize=True);
	out[:,1] = out[:,1]+1;
	return out;