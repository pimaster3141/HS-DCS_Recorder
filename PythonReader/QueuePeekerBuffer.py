import threading
import queue

class QueuePeeker(threading.Thread):

	def __init__(self, bufferIn, bufferOut, bufferPeek):
		threading.Thread.__init__(self);

		self._inBuffer = bufferIn;
		self._outBuffer = bufferOut;
		self._peekBuffer = bufferPeek;

		self._isAlive = True;

	def run(self):
		print("Starting Peeker");

		while(self._isAlive):
			try:
				temp = self._inBuffer.get(block=True, timeout=1);
				self._outBuffer.put_nowait(temp);
				# if(self._peekBuffer.empty()):
				if(self._peekBuffer.qsize() < 3):
					self._peekBuffer.put_nowait(temp);
					
			except queue.Empty:
				continue;
			except Exception as e:
				print(e);
				break;

		print("Peeker Closed");

	def shutdown(self):
		self._isAlive = False;
		self.join();


