import multiprocessing as mp
import array
import queue


class DataHandler(mp.Process):
	_TIMEOUT = 1

	def __init__(self, MPI, dataPipe, bufferSize, packetSize, filename=None):
		mp.Process.__init(self);

		self.MPI = MPI;
		self.dataPipe = dataPipe;

		self.dataBuffer = array.array('h', [0]*(bufferSize/packetSize));

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
		self.shutdown();
		self.join();


	def getRealtimeQueue(self):
		return self.realtimeQueue;

	def enableRealtime(self):
		self.realtimeData = True;

	def disableRealtime(self):
		self.realtimeData = False;

