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

		self.tauList = G2Calc.mtAuto(np.ones(int(bufferSize/sampleSize)*packetMultiple), fs=fs, levels=G2_LEVELS);
		self.SNRBuffer = np.ones((SNRBufferDepth, length(self.tauList)));
		self.SNRBuffer[0] = np.zeros(length(self.tauList));

		self.fs = fs;
		self.pool = mp.Pool(processes=self.numProcessors);

		self.g2Buffer = mp.Queue(QUEUE_DEPTH);
		self.countBuffer = mp.Queue(QUEUE_DEPTH);
		self.flowBuffer = mp.Queue(QUEUE_DEPTH);

		
		self.isDead = mp.Event();

	def run(self):
		try:
			initialData = np.zeros(self.packetSize*self.packetMultiple, dtype=npDtype);
			g2Fcn = partial(G2Extract.calculateG2, fs=self.fs, levels=G2_LEVELS, legacy=self.legacy);

			while(not self.isDead.is_set()):
				for i in range(self.packetMultiple):
					initialData[i*packetSize:i*(packetSize+1)] = self.inputBuffer.get(block=True, timeout=QUEUE_TIMEOUT);


				inWaiting = int(inputBuffer.qsize()/self.packetMultiple);
				data = np.zeros((inWaiting+1, self.packetSize*self.packetMultiple), dtype=npDtype)
				data[0] = initialData;

				for i in range(inWaiting):
					for j in range(self.packetMultiple):
						data[i+1][j*packetSize:j*(packetSize+1)] = self.inputBuffer.get_nowait();

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
		self.isDead.set();
		self.pool.close();
		self.pool.join();

	def stop(self):
		if(not self.isDead.is_set()):
			self.isDead.set();
			self.join();
			try:
				self.MPI.put_nowait("Stopping Processor");
			except Exception as ei:
				pass

	def getBuffers(self):
		return self.g2Buffer, self.countBuffer, self.flowBuffer;

	def getTauList(self):
		return self.tauList;
