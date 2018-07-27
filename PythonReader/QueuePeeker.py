import threading
import queue

class QueuePeeker(threading.Thread):

	def __init__(self, bufferIn, bufferOut):
		threading.Thread.__init__(self);

		self._inBuffer = bufferIn;
		self._outBuffer = bufferOut;

		self._dataHold = None;
		self._dataLock = threading.Lock();

		self._isAlive = True;

	def run(self):
		print("Starting Peeker");

		while(self._isAlive and self._dataHold == None):
			self._dataLock.acquire();
			try:
				self._dataHold = self._inBuffer.get(block=True, timeout=1);
			except queue.Empty:
				continue;
			except Exception as e:
				print(e);
				break;
			finally:
				self._dataLock.release();

		while(self._isAlive):
			self._dataLock.acquire();
			try:
				temp = self._inBuffer.get(block=True, timeout=1);
				self._outBuffer.put_nowait(self._dataHold);
				self._dataHold = temp;
			except queue.Empty:
				continue;
			except Exception as e:
				print(e);
				break;
			finally:
				self._dataLock.release();

		print("Peeker Closed");

	def shutdown(self):
		self._isAlive = False;
		self.join();

	def peek(self):
		if(self._isAlive == False):
			return ''
		else:
			output = None;
			self._dataLock.acquire();
			try:
				output = self._dataHold;
			except Exception as e:
				print(e);
			finally:
				self._dataLock.release();

			return output;


