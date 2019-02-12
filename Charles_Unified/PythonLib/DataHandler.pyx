import multiprocessing as mp
import array
import queue


class DataHandler(mp.Process):
	_TIMEOUT = 1

	def __init__(self, MPI, dataPipe, bufferSize, sampleSize=2, filename=None):
		mp.Process.__init(self);

		self.sampleSizeCode = None;
		if(sampleSize == 2):
			self.sampleSizeCode = 'h';
		else:
			raise Exception("Sample Size Code not implemented");

		self.MPI = MPI;
		self.dataPipe = dataPipe;if(int(bufferSize/sampleSize)*sampleSize != bufferSize):
			raise Exception("Sample Size not integer multiple of buffer size");

		if(int(bufferSize/sampleSize)*sampleSize != bufferSize):
			raise Exception("Sample Size not integer multiple of buffer size");

		self.dataBuffer = array.array(self.sampleSizeCode, [0]*(bufferSize/sampleSize));

		self.realtimeData = False;
		self.realtimeQueue = mp.Queue(1000);

		self.outFile = None;
		self.debug = True;
		if(filename != None):
			self.outFile = open(filename, 'wb');
			self.debug = False;

		self.isAlive = True;


	def run(self):
		try: 
			while(self.isAlive):
				if(self.dataPipe.poll(DataHandler._TIMEOUT)):
					self.dataPipe.recv_bytes_into(self.dataBuffer);

					if(not self.debug):
						self.dataBuffer.tofile(self.outFile);

					if(self.realtimeData):
						if(not self.realtimeQueue.full()):
							self.realtimeQueue.put_nowait(self.dataBuffer);
						else:
							self.MPI.put_nowait("Realtime Buffer Overrun");

		except Exception as e:
			try:
				self.MPI.put_nowait(e);
			except Exception as ei:
				pass
		finally:
			self.shutdown();

	def shutdown(self):
		self.isAlive = False;
		self.outFile.close();

	def stop(self):
		if(self.isAlive):
			self.shutdown();
			self.join();
			try:
				self.MPI.put_nowait("Stopping Handler");
			except Exception as ei:
				pass

	def getRealtimeQueue(self):
		return self.realtimeQueue;

	def enableRealtime(self):
		self.realtimeData = True;

	def disableRealtime(self):
		self.realtimeData = False;

