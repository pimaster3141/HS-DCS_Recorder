import multipletau as mt
import numpy as np

class MTau():
	def __init__(self, fs, windowSize, windowShift):
		self._fs = fs;
		self._windowSize = windowSize;
		self._windowShift = windowShift;

		self._previousWindow = np.zeros(windowSize, dtype=np.uint8);
		self._leftovers = np.array([], dtype=np.uint8);

	def update(self, data):
		output = [];

		while((len(self._leftovers) + len(data)) >= self._windowShift):
			self._previousWindow = np.append(
				self._previousWindow[self._windowShift:],
				self._leftovers
				);

			self._previousWindow = np.append(
				self._previousWindow,
				data[:(self._windowShift - len(self._leftovers))]
				);

			data = data[self._windowShift-len(self._leftovers):];
			self._leftovers = np.array([], dtype=np.uint8);

			# output.append(self._previousWindow);
			output.append(mtAuto(self._previousWindow, fs=self._fs));

		self._leftovers = np.append(self._leftovers, data);

		# print(self._leftovers);
		# print(self._previousWindow);

		return output;



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