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
import multiprocessing as mp
import os
print("Done");

def init(inFile, outFile):
	MPIFX3 = mp.Queue();
	MPIHandler = mp.Queue();

	dev = FX3.Emulator(MPIFX3, inFile);
	pipe = dev.getPipe();
	buffSize = dev.getBufferSize();

	handler = DataHandler.DataHandler(MPIHandler, pipe, buffSize, filename=outFile);

	return (MPIFX3, MPIHandler, dev, handler);

def run(dev, handler):
	dev.start();
	handler.start();

def stop(dev, handler):
	dev.stop();
	handler.stop();
