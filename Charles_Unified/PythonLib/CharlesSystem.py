import setuptools
import pyximport; pyximport.install()

import usb
import FX3
import DataHandler
import DataProcessor
import Display
import multiprocessing as mp

class CharlesSystem():
	VENDOR_ID = 0x04B4;
	PRODUCT_IDs = [0x00F1,0x00F0];
	ENDPOINT_ID = 0x81;
	
	def __init__(self, outFile, version=2):
		self.dev = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_IDs[version-1]);
		if(self.dev == None):
			raise Exception("NO DEVICE ATTACHED");

		self.dev.set_configuration();
		self.outFile = outFile;

		self.MPIFX3 = mp.Queue();
		self.MPIHandler = mp.Queue();
		self.MPIProcessor = mp.Queue();
