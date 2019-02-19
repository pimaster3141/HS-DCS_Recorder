import threading
import time
import G2Display;

class ThreadWorker(threading.Thread):

	def __init__(self, bufferPeek, sampleCLK=10E6, numChannels=1, refreshRate=20, bufferDepth=10):
		threading.Thread.__init__(self);

		self._bufferPeek = bufferPeek;
		self._sampleCLK = sampleCLK;
		self._numChannels = numChannels;
		self._refreshRate = refreshRate;
		self._bufferDepth = bufferDepth;

	def run(self):
		print("Starting Thread");

		self._display = G2Display.G2GraphWindow(self._bufferPeek, self._sampleCLK, self._numChannels, self._refreshRate, self._bufferDepth);
		# self._display.run();

		time.sleep(10);

		print("Stopping Thread");

	def shutdown(self):
		self.stopThreads();

	def stopThreads(self):
		return;
