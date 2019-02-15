import multiprocessing as mp
import array
import queue
import time

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
					print("1");
					self.dataPipe.recv_bytes_into(self.dataBuffer);
					print("2");

					if(not self.debug):
						print("3.1")
						self.dataBuffer.tofile(self.outFile);
						print("3.2");

					if(self.realtimeData.is_set()):
						print("data in");
						if(not self.realtimeQueue.full()):
							print("4.1");
							self.realtimeQueue.put_nowait(self.dataBuffer);
							print("Data Placed");
							pass
						else:
							print("4.2");
							print("FULL!");
							self.MPI.put_nowait("Realtime Buffer Overrun");
							print("4.3");
							self.realtimeData.clear();
							print("4.4");
					print("5");
				print("6");

		except Exception as e:
			print("e.1");
			try:
				print("e.2");
				self.MPI.put_nowait(e);
				print("e.2");
			except Exception as ei:
				print(ei);
				pass
		finally:
			print("7");
			self.shutdown();
			print("8");

		print("9");
		return;

	def shutdown(self):
		self.isDead.set();
		self.outFile.close();
		
		time.sleep(0.5);
		while(True):
			try:
				(self.realtimeQueue.get(False));
			except queue.Empty:
				time.sleep(0.5)    # Give tasks a chance to put more data in
				if not self.realtimeQueue.empty():
					continue
				else:
					break;

	def stop(self):
		print("s.1");
		if(not self.isDead.is_set()):
			print("S.2");
			self.isDead.set();
			print("S.3");
			self.join();
			print("S.4");
			try:
				print("S.5");
				self.MPI.put_nowait("Stopping Handler");
				print("S.6");
			except Exception as ei:
				pass

	def getRealtimeQueue(self):
		return self.realtimeQueue;

	def enableRealtime(self):
		self.realtimeData.set();

	def disableRealtime(self):
		self.realtimeData.clear();

