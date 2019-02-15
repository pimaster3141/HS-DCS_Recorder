from sys import platform
if platform == "linux" or platform == "linux2":
    pass
elif platform == "darwin":
    raise Exception("Unsupported OS: " + str(platform));
elif platform == "win32":
    raise Exception("Unsupported OS: " + str(platform));

print("Compiling and Loading Libraries...")
import sys
sys.path.insert(0, 'PythonLib');
import setuptools
import pyximport; pyximport.install()

import FX3
import DataHandler
import DataProcessor
import multiprocessing as mp
import os
import code
import time
print("Done");



MPIFX3 = None;
MPIHandler = None;
MPIProcessor = None;
dev = None;
handler = None;
processor = None;

def init(inFile, outFile):
	global MPIFX3, MPIHandler, MPIProcessor
	global dev, handler, processor
	MPIFX3 = mp.Queue();
	MPIHandler = mp.Queue();
	MPIProcessor = mp.Queue();

	dev = FX3.Emulator(MPIFX3, inFile);
	pipe = dev.getPipe();
	buffSize = dev.getBufferSize();

	handler = DataHandler.DataHandler(MPIHandler, pipe, buffSize, filename=outFile);
	realtime = handler.getRealtimeQueue();
	handler.enableRealtime();

	processor = DataProcessor.DataProcessor(MPIProcessor, realtime, [[0,0]], legacy=False, fs=2.5E6, bufferSize=buffSize);

	# return (MPIFX3, MPIHandler, MPIProcessor, dev, handler, processor);

def run():
	global MPIFX3, MPIHandler, MPIProcessor
	global dev, handler, processor
	processor.start();
	handler.start();
	dev.start();

def stop():
	global MPIFX3, MPIHandler, MPIProcessor
	global dev, handler, processor
	dev.stop();
	dev.join();
	print("dev stop");
	handler.stop();
	handler.join();
	print("handler stop");
	processor.stop();
	processor.join()
	print("processor stop");

def qstat():
	global MPIFX3, MPIHandler, MPIProcessor
	global dev, handler, processor
	print(MPIFX3.qsize());
	print(MPIHandler.qsize());
	print(MPIProcessor.qsize());

def readAll():
	s = MPIFX3.qsize();
	for i in range(s):
		print(MPIFX3.get());

	print("");
	s = MPIHandler.qsize();
	for i in range(s):
		print(MPIHandler.get());

	print("");
	s = MPIProcessor.qsize();
	for i in range(s):
		print(MPIProcessor.get());



# init('../Charles2/PythonReader/output/test', 'testDebug');
init('../Charles2/PythonReader/output/test', None);
code.interact(local = locals());
