import multiprocessing as mp
import array
import queue

import threading


class DataHandler(mp.Process):
# class DataHandler(threading.Thread):
	_TIMEOUT = 1
	QUEUE_DEPTH = 100;

	def __init__(self, MPI, dataPipe, bufferSize, sampleSize=2, filename=None):
		mp.Process.__init__(self);
		# threading.Thread.__init__(self);

		self.sampleSizeCode = None;
		if(sampleSize == 2):
			self.sampleSizeCode = 'h';
		else:
			raise Exception("Sample Size Code not implemented");

		self.MPI = MPI;
		self.dataPipe = dataPipe;
		if(int(bufferSize/sampleSize)*sampleSize != bufferSize):
			raise Exception("Sample Size not integer multiple of buffer size");

		self.dataBuffer = array.array(self.sampleSizeCode, [0]*int(bufferSize/sampleSize));

		self.realtimeData = mp.Event();
		self.realtimeQueue = mp.Queue(DataHandler.QUEUE_DEPTH);

		self.outFile = None;
		self.debug = True;
		if(filename != None):
			self.outFile = open(filename, 'wb');
			self.debug = False;

		self.isDead = mp.Event();


	def run(self):
		try: 
			while(not self.isDead.is_set()):
				print("go");
				if(self.dataPipe.poll(DataHandler._TIMEOUT)):
					self.dataPipe.recv_bytes_into(self.dataBuffer);

					if(not self.debug):
						self.dataBuffer.tofile(self.outFile);

					if(self.realtimeData.is_set()):
						print("data in");
						if(not self.realtimeQueue.full()):
							self.realtimeQueue.put_nowait(self.dataBuffer);
							print("Data Placed");
							pass
						else:
							print("FULL!");
							self.MPI.put_nowait("Realtime Buffer Overrun");
							self.realtimeData.clear();

		except Exception as e:
			try:
				self.MPI.put_nowait(e);
			except Exception as ei:
				pass
		finally:
			self.shutdown();

	def shutdown(self):
		self.isDead.set();
		self.outFile.close();

	def stop(self):
		if(not self.isDead.is_set()):
			self.isDead.set();
			self.join();
			try:
				self.MPI.put_nowait("Stopping Handler");
			except Exception as ei:
				pass

	def getRealtimeQueue(self):
		return self.realtimeQueue;

	def enableRealtime(self):
		self.realtimeData.set();

	def disableRealtime(self):
		self.realtimeData.clear();

