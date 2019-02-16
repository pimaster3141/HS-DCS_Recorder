import setuptools
import pyximport; pyximport.install()
import multiprocessing as mp
import HSDCSParser
import numpy as np
import os
from functools import partial
# import G2Extract
import G2Calc
import queue
import time

import threading

class DataProcessor(mp.Process):
# class DataProcessor(threading.Thread):
	QUEUE_TIMEOUT = 1;
	QUEUE_DEPTH = 100;
	G2_LEVELS = 8;

	def __init__(self, MPI, inputBuffer, averages, legacy, fs, bufferSize, sampleSize=2, packetMultiple=2, calcFlow=False, SNRBufferDepth=50, numProcessors=None):
		mp.Process.__init__(self);
		# threading.Thread.__init__(self);
		self.MPI = MPI;
		self.inputBuffer = inputBuffer;
		self.averages = averages
		self.legacy = legacy;
		self.fs = fs;
		self.packetMultiple = packetMultiple;
		self.calcFlow = calcFlow;

		self.npDtype = None;
		if(sampleSize == 2):
			self.npDtype = np.int16;
		else:
			raise Exception("Sample Size Code not implemented");

		self.numProcessors = numProcessors;
		if(numProcessors==None):
			self.numProcessors = os.cpu_count();

		self.packetSize = int(bufferSize/sampleSize);
		self.tauList = G2Calc.mtAuto(np.ones(self.packetSize*packetMultiple), fs=fs, levels=DataProcessor.G2_LEVELS)[:,0];
		self.SNRBuffer = np.ones((SNRBufferDepth, len(self.tauList)));
		self.SNRBuffer[0] = np.zeros(len(self.tauList));


		self.g2Buffer = mp.Queue(DataProcessor.QUEUE_DEPTH);
		# self.countBuffer = mp.Queue(DataProcessor.QUEUE_DEPTH);
		self.flowBuffer = mp.Queue(DataProcessor.QUEUE_DEPTH);

		
		self.isDead = mp.Event();

	def run(self):
		try:
			self.pool = mp.Pool(processes=self.numProcessors);
			initialData = np.zeros(self.packetSize*self.packetMultiple, dtype=self.npDtype);
			g2Fcn = partial(G2Calc.calculateG2, fs=self.fs, levels=DataProcessor.G2_LEVELS, legacy=self.legacy);

			while(not self.isDead.is_set()):				
				try:
					for i in range(self.packetMultiple):
						initialData[i*self.packetSize:(i+1)*self.packetSize] = self.inputBuffer.get(block=True, timeout=DataProcessor.QUEUE_TIMEOUT);
				except queue.Empty:					
					continue
				
				inWaiting = int(self.inputBuffer.qsize()/self.packetMultiple);	
				# print(inWaiting);			
				data = np.zeros((inWaiting+1, self.packetSize*self.packetMultiple), dtype=self.npDtype)
				data[0] = initialData;
				
				try:
					for i in range(inWaiting):
						for j in range(self.packetMultiple):
							data[i+1][j*self.packetSize:(j+1)*self.packetSize] = self.inputBuffer.get(block=True, timeout=DataProcessor.QUEUE_TIMEOUT);
				except queue.Empty:
					pass

				g2Data = self.pool.map(g2Fcn, data);
				try:
					self.g2Buffer.put_nowait(g2Data); #(g2, vap)
				except queue.Full:
					pass

				# print(len(g2Data[0][0][0]))
				# time.sleep(0.2)

				if(self.calcFlow):
					pass

			# print("IM DYING!!! But its natural");
			

		except Exception as e:
			# print("SHITBALLS IM MURDERED");
			# raise(e);
			try:
				self.MPI.put_nowait(e);
			except Exception as ei:
				pass
		finally:			
			self.shutdown();

	def shutdown(self):
		self.isDead.set();
		self.pool.close();
		self.pool.terminate();		
		self.pool.join();		
		
		time.sleep(0.5);
		while(True):
			try:
				(self.g2Buffer.get(False));
			except queue.Empty:
				time.sleep(0.5)    # Give tasks a chance to put more data in
				if not self.g2Buffer.empty():
					continue
				else:
					break;
		while(True):
			try:
				(self.flowBuffer.get(False));
			except queue.Empty:
				time.sleep(0.5)    # Give tasks a chance to put more data in
				if not self.flowBuffer.empty():
					continue
				else:
					break;

		self.g2Buffer.close();
		self.flowBuffer.close();
		self.g2Buffer.cancel_join_thread();
		self.flowBuffer.cancel_join_thread();
		try:
			self.MPI.put_nowait("Stopping Processor");
			time.sleep(1);
		except Exception as ei:
			pass
		finally:
			self.MPI.close();
			self.MPI.cancel_join_thread();

	def stop(self):
		if(not self.isDead.is_set()):
			self.isDead.set();			
			# self.join();

	def getBuffers(self):
		return self.g2Buffer, self.flowBuffer;

	def getTauList(self):
		return self.tauList;

	def getFs(self):
		return self.fs;

	def getTWindow(self):
		return self.packetSize*self.packetMultiple/self.fs;

	def isFlowEnabled(self):
		return self.calcFlow;

