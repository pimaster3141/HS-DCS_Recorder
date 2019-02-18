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
	BENCHMARK_SIZE = 5242880; # should be 10s at 2.5MHz
	BYTES_PER_SAMPLE = 2;

	
	def __init__(self, outFile, version=None, fs=None, averages=[[0, 3]], demo=False):
		
		self.isStarted = False;
		devices, kind = findDevices(version);
		self.dev = devices[0];
		self.legacy = kind[0];
		self.dev.set_configuration();
		self.outFile = outFile;

		self.fs = fs;
		if(self.fs == None):
			self.fs = self.bench();
			print("Device is " + str(self.fs/1E6) + "Msps");

		if(not outFile==None):
			with open(str(outFile)+".params", 'w') as f:
				f.write("fs="+str(self.fs)+"\n");
				f.write("legacy="+str(self.legacy)+"\n");
				f.write("averages="+str(averages)+"\n");

		self.MPIFX3 = mp.Queue();
		self.MPIHandler = mp.Queue();
		self.MPIProcessor = mp.Queue();

		self.FX3 = None;
		if(demo):
			self.FX3 = FX3.Emulator(self.MPIFX3, '../Charles2/PythonReader/output/japan_flat');
		else:
			self.FX3 = FX3.DCS(self.MPIFX3, self.dev)

		fxPipe = self.FX3.getPipe();
		fxBufferSize = self.FX3.getBufferSize();
		self.handler = DataHandler.DataHandler(self.MPIHandler, fxPipe, fxBufferSize, sampleSize=CharlesSystem.BYTES_PER_SAMPLE, filename=self.outFile);

		handlerBuffer = self.handler.getRealtimeQueue();
		self.handler.enableRealtime();
		self.processor = DataProcessor.DataProcessor(self.MPIProcessor, handlerBuffer, averages, self.legacy, self.fs, fxBufferSize, sampleSize=CharlesSystem.BYTES_PER_SAMPLE, calcFlow=True);


		print("Device Initialized!");		

	def stop(self):
		if(self.isStarted):
			print("Device already halted");
			return;

		print("Halting Device");
		self.FX3.stop();
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

		self.display = Display.GraphWindow(self.processor, self.legacy, stopFcn=self.stop);

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
			# try:
			self.dev.read(0x81, 524288, 5000);
			s = time.time();
			self.dev.read(0x81, CharlesSystem.BENCHMARK_SIZE, 20000);
			e = time.time();
			# except Exception as e:
			# 	raise Exception("UNKNOWN HARDWARE ERROR");

			return int((CharlesSystem.BENCHMARK_SIZE/CharlesSystem.BYTES_PER_SAMPLE)/(e-s));


def findDevices(version):
	devicesGen = None;
	if(version == None):
		devicesGen = usb.core.find(idVendor=CharlesSystem.VENDOR_ID, find_all=True);
	elif(version == 1):
		devicesGen = usb.core.find(idVendor=CharlesSystem.VENDOR_ID, idProduct=CharlesSystem.PRODUCT_IDs[0], find_all=True);
	elif(version == 2):
		devicesGen = usb.core.find(idVendor=CharlesSystem.VENDOR_ID, idProduct=CharlesSystem.PRODUCT_IDs[1], find_all=True);
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
