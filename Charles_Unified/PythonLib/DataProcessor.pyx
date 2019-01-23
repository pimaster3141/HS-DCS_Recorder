import setuptools
import pyximport; pyximport.install()
import multiprocessing as mp
import HSDCSParser

class DataProcessor(mp.Process):

	def __init__(self, MPI, dataBuffer, legacy):
		self.MPI = MPI;
		self.dataBuffer = dataBuffer;



		self.isAlive = True;