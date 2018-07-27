import multiprocessing
import time
import G2Display
import DCSReader
import BufferedWriter
import QueuePeekerBuffer
import QueuePeeker
from multiprocessing import Queue as Q
import queue

class MPWorker(multiprocessing.Process):

	def __init__(self, comPipe, fileName, dataQueue):
		multiprocessing.Process.__init__(self);

		self._peekBuf = dataQueue;
		self._comPipe = comPipe;
		self._filename = fileName;

	def run(self):
		# print("Starting Process");

		self._inBuf = queue.Queue();
		self._outBuf = queue.Queue();
		# self._peekBuf = Q();

		self._DCS = DCSReader.DCSReader(self._inBuf);
		# self._peeker = QueuePeeker.QueuePeeker(self._inBuf, self._outBuf);
		self._peeker = QueuePeekerBuffer.QueuePeeker(self._inBuf, self._outBuf, self._peekBuf);
		self._outFile = BufferedWriter.BufferedWriter(self._outBuf, self._filename);
		# display = MPWorker.MPWorker(peekBuf, sampleClk, numChannels, refreshRate, bufferDepth);
		# display = ThreadWorker.ThreadWorker(peekBuf, sampleClk, numChannels, refreshRate, bufferDepth);
		# display = G2Display.G2GraphWindow(peekBuf, sampleClk, numChannels, refreshRate, bufferDepth)

		self._outFile.start();
		self._peeker.start();
		self._DCS.start();

		self._comPipe.recv()

		self._DCS.shutdown();
		self._peeker.shutdown();
		self._outFile.shutdown();

		# print("Stopping Process");

		del(self._DCS);
		del(self._peeker);
		del(self._outFile);

		self._comPipe.send("done");
		return;

	def shutdown(self):
		self.stopThreads();

	def stopThreads(self):
		return;
