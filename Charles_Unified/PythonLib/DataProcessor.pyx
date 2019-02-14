import setuptools
import pyximport; pyximport.install()
import multiprocessing as mp
import HSDCSParser
import numpy as np
import os
from functools import partial
import G2Extract

class DataProcessor(mp.Process):

	QUEUE_TIMEOUT = 2000;
	QUEUE_DEPTH = 100;
	G2_LEVELS = 8;

	def __init__(self, MPI, inputBuffer, averages, legacy, fs, bufferSize, sampleSize=2, packetMultiple=1, calcFlow=True, SNRBufferDepth=50 numProcessors=None):
		mp.Process.__init__(self);
		self.MPI = MPI;
		self.inputBuffer = inputBuffer;
		self.legacy = legacy;
		self.packetMultiple = packetMultiple;
		self.calcFlow = calcFlow;

		self.npDtype = None;
		if(sampleSize == 2):
			self.npDtype = np.int16;
		else:
			raise Exception("Sample Size Code not implemented");

		self.numProcessors = numProcessors;
		if(numProcessors==None):
			self.numProcessors = os.cpu_count;

		self.tauList = G2Calc.mtAuto(np.ones(int(bufferSize/sampleSize)), fs=fs, levels=G2_LEVELS);
		self.SNRBuffer = np.zeros((SNRBufferDepth, ))
		for i in range(SNRBufferDepth):

		self.fs = fs;
		self.pool = mp.Pool(processes=self.numProcessors);

		self.g2Buffer = mp.Queue(QUEUE_DEPTH);
		self.countBuffer = mp.Queue(QUEUE_DEPTH);
		self.flowBuffer = mp.Queue(QUEUE_DEPTH);

		
		self.isAlive = True;

	def run(self):
		try:
			initialData = np.zeros(self.packetSize*self.packetMultiple, dtype=npDtype);
			g2Fcn = partial(G2Extract.calculateG2, fs=self.fs, levels=G2_LEVELS, legacy=self.legacy);
			flowFcn = partial(G2Extract.calculateG2, fs=self.fs, levels=G2_LEVELS, legacy=self.legacy);
			while(self.isAlive):
				for i in range(self.packetMultiple):
					initialData[i*packetSize:i*(packetSize+1)] = self.inputBuffer.get(block=True, timeout=QUEUE_TIMEOUT);


				inWaiting = int(inputBuffer.qsize()/self.packetMultiple);
				data = np.zeros((inWaiting+1, self.packetSize*self.packetMultiple), dtype=npDtype)
				data[0] = initialData;

				for i in range(inWaiting):
					for j in range(self.packetMultiple):
						data[i+1][i*packetSize:i*(packetSize+1)] = self.inputBuffer.get_nowait();


				g2Data = self.pool.map(g2Fcn, data);

				self.g2Buffer.put_nowait(g2Data);

				if(self.calcFlow):
					flowData = self.pool.map()

		except Exception as e:
			try:
				self.MPI.put_nowait(e);
			except Exception as ei:
				pass
		finally:
			self.shutdown();

	def shutdown(self):
		self.isAlive = False;
		self.pool.close();
		self.pool.join();

	def stop(self):
		if(self.isAlive):
			self.shutdown();
			self.join();
			try:
				self.MPI.put_nowait("Stopping Processor");
			except Exception as ei:
				pass

	def getBuffers(self):
		return self.g2Buffer, self.flowBuffer;
