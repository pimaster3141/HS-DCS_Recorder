import setuptools
import pyximport; pyximport.install()
import multiprocessing as mp
import HSDCSParser
import numpy as np
import os

class DataProcessor(mp.Process):

	QUEUE_TIMEOUT = 2000;
	G2_LEVELS = 8;

	def __init__(self, MPI, inputBuffer, legacy, fs, packetMultiple=1, sampleSize=2, calcFlow=True, numProcessors=None):
		mp.Process.__init__(self);
		self.MPI = MPI;
		self.inputBuffer = inputBuffer;

		self.packetMultiple = packetMultiple;

		self.npDtype = None;
		if(sampleSize == 2):
			self.npDtype = np.int16;
		else:
			raise Exception("Sample Size Code not implemented");

		self.numProcessors = numProcessors;
		if(numProcessors==None):
			self.numProcessors = os.cpu_count;

		self.fs = fs;
		
		self.pool = mp.Pool(processes=self.numProcessors);


		self.isAlive = True;


	def run(self):


		try:
			initialData = np.zeros(self.packetSize*self.packetMultiple, dtype=npDtype);
			while(self.isAlive):
				for i in range(self.packetMultiple):
					initialData[i*packetSize:i*(packetSize+1)] = self.inputBuffer.get(block=True, timeout=QUEUE_TIMEOUT);


				inWaiting = int(inputBuffer.qsize()/self.packetMultiple);
				data = np.zeros((inWaiting+1, self.packetSize*self.packetMultiple), dtype=npDtype)
				data[0] = initialData;

				for i in range(inWaiting):
					for j in range(self.packetMultiple):
						data[i+1][i*packetSize:i*(packetSize+1)] = self.inputBuffer.get_nowait();

				# data = np.ravel(data);

				channel = None;
				vap = None;
				if(legacy):
					channel, vap = HSDCSParser.parseCharlesLegacy(data);
				else:
					channel, vap = HSDCSParser.parseCharles2(data);

				g2Data = G2Calc.mtAutoQuad(channel, self.fs, G2_LEVELS);
				vap = np.array((np.mean(vap, axis=1)+0.5), dtype=np.int8);
				

		except Exception as e:
			try:
				self.MPI.put_nowait(e);
			except Exception as ei:
				pass
		finally:
			self.shutdown();


	def shutdown(self):
		self.isAlive = False;
		self

	def stop(self):
		self.shutdown();
		self.join();

