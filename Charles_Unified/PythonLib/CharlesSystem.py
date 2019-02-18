from sys import platform
if platform == "linux" or platform == "linux2":
    pass
elif platform == "darwin":
    raise Exception("Unsupported OS: " + str(platform));
elif platform == "win32":
    raise Exception("Unsupported OS: " + str(platform));

print("Compiling and Loading Libraries...")

import setuptools
import pyximport; pyximport.install()

import usb
import FX3
import DataHandler
import DataProcessor
import Display
import multiprocessing as mp
import time
print("Done")

class CharlesSystem():
	VENDOR_ID = 0x04B4;
	PRODUCT_IDs = [0x00F1,0x00F0];
	BENCHMARK_SIZE = 52428800; # should be 10s at 2.5MHz
	BYTES_PER_SAMPLE = 2;

	
	def __init__(self, outFile, version=None, fs=None, averages=[[0, 3]]):
		devices, kind = findDevices(version);
		self.dev = devices[0];
		self.legacy = kind[0];
		self.dev.set_configuration();
		self.outFile = outFile;

		self.fs = fs;
		if(self.fs == None):
			self.fs = self.bench();

		self.MPIFX3 = mp.Queue();
		self.MPIHandler = mp.Queue();
		self.MPIProcessor = mp.Queue();

		self.FX3 = FX3.DCS(self.MPIFX3, self.dev)

		fxPipe = self.FX3.getPipe();
		fxBufferSize = self.FX3.getBufferSize();
		self.handler = DataHandler.DataHandler(self.MPIHandler, fxPipe, fxBufferSize, sampleSize=BYTES_PER_SAMPLE, filename=self.outFile);

		handlerBuffer = self.handler.getRealtimeQueue();
		self.handler.enableRealtime();
		self.processor = DataProcessor.DataProcessor(self.MPIProcessor, handlerBuffer, averages, self.legacy, self.fs, fxBufferSize, sampleSize=BYTES_PER_SAMPLE, calcFlow=True);

		self.display = Display.GraphWindow(self.processor, self.legacy, stopFcn=self.stop);

		self.isStarted = False;
		print("Device Initialized!");		

	def stop(self):
		if(self.isStarted):
			print("Device already halted");
			return;

		print("Halting Device");
		self.dev.stop();
		self.handler.stop();
		self.processor.stop();
		self.display.stop();

		self.dev.join();
		self.handler.join();
		self.processor.join();


		s = self.MPIFX3.qsize();
		for i in range(s):
			try:
				print(self.MPIFX3.get());
			except Exception as e:
				print("WARNING: ")
				print(e);
				continue;

		print("");
		s = self.MPIHandler.qsize();
		for i in range(s):
			try:
				print(self.MPIHandler.get());
			except Exception as e:
				print("WARNING: ")
				print(e);
				continue;

		print("");
		s = self.MPIProcessor.qsize();
		for i in range(s):
			try:
				print(self.MPIProcessor.get());
			except Exception as e:
				print("WARNING: ")
				print(e);
				continue;

		self.device.reset();
		usb.util.dispose_resources(self.device);
		print("Device Halted");

	def start(self):
		if(self.isStarted):
			print("Device already running");
			return;

		self.isStarted = True;
		print("Starting Charles!");
		processor.start();
		handler.start();
		dev.start();
		display.run();

	def bench(self):
		if(self.isStarted):
			raise Exception("Cannot benchmark after start");
		else:
			print("Benchmarking Device ~10s");
			s = 0.0;
			e = 0.0;
			try:
				dev.read(0x81, 524288, 500);
				s = time.time();
				dev.read(0x81, BENCHMARK_SIZE, 20000);
				e = time.time();
			except:
				raise Exception("UNKNOWN HARDWARE ERROR");

			return int((BENCHMARK_SIZE/BYTES_PER_SAMPLE)/(e-s));


def findDevices(version):
	devicesGen = None;
	if(version == None):
		devicesGen = usb.core.find(idVendor=VENDOR_ID, find_all=True);
	elif(version == 1):
		devicesGen = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_IDs[0], find_all=True);
	elif(version == 2):
		devicesGen = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_IDs[1], find_all=True);
	else:
		raise Exception("UNSUPPORTED VERSON" + str(version));

	devices = [];
	legacy = []
	for dev in devicesGen:
		devices.append(dev);
		legacy.append(dev.idProduct == CharlesSystem.PRODUCT_IDs[0]);

	if(len(devices) == 0):
		raise Exception("CANNOT FIND DEVICE");

	return devices, legacy;
