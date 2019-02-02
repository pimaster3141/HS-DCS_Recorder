import setuptools
import pyximport; pyximport.install()
import multiprocessing as mp
import HSDCSParser
import numpy as np

class DataProcessor(mp.Process):

	def __init__(self, MPI, inputBuffer, legacy, bufferSize, sampleSize=2, numProcessors=None):
		mp.Process.__init__(self);
		self.MPI = MPI;
		self.inputBuffer = inputBuffer;

		if(int(bufferSize/sampleSize)*sampleSize != bufferSize):
			raise Exception("Sample Size not integer multiple of buffer size");
		self.packetSize = buffersize/sampleSize;

		self.npDtype = None;
		if(sampleSize == 2):
			self.npDtype = np.int16;
		else:
			raise Exception("Sample Size Code not implemented");

		self.numProcessors = numProcessors;
		if(numProcessors==None):
			self.numProcessors = mp.cpu_count;


		self.isAlive = True;


	def run(self):
		pool = mp.Pool(processes=self.numProcessors);


		try:
			while(self.isAlive):
				inWaiting = inputBuffer.qsize();
				data = np.zeros((inWaiting, self.packetSize), dtype=npDtype)

				for i in range(inWaiting):
					data[i] = self.inputBuffer.get_nowait();

				data = np.ravel(data);

				channel = None;
				vap = None;
				if(legacy):
					channel, vap = HSDCSParser.parseCharlesLegacy(data);
				else:
					channel, vap = HSDCSParser.parseCharles2(data);

				