import multiprocessing as mp
import usb.core
import usb.util
import array
import time

class DCS(mp.Process):
	_TIMEOUT = 2000;
	_READ_SIZE = 262144;	#512KB = 524288 base2

	_ENDPOINT_ID = 0x81;

	def __init__(self, MPI, device, bufferSize=DCS._READ_SIZE):
		mp.Process.__init__(self);

		self.MPI = MPI;
		self.device = device;
		self.bufferSize = bufferSize;
		(self.pipeOut, self.pipeIn) = mp.Pipe(duplex=False);
		self._packet = usb.util.create_buffer(self.bufferSize);
		self.isAlive = True;


	def run(self):
		try:
			self.device.read(DCS._ENDPOINT_ID, 524288, DCS._TIMEOUT);
		except Exception as e:
			try:
				self.MPI.put_nowait(e);
			except Exception as ei:
				pass
			finally:
				self.shutdown();
			
		try:
			while(self.isAlive):
				# self.pipeOut.send_bytes(self._dev.read(DCS._ENDPOINT_ID, self.bufferSize, DCS._TIMEOUT));
				numRead = self.device.read(DCS._ENDPOINT_ID ,self._packet, DCS._TIMEOUT);
				if((numRead) != self.bufferSize):
					raise Exception("Device not ready");
				self.pipeOut.send_bytes(self._packet);
		except Exception as e:
			try:
				self.MPI.put_nowait(e);
			except Exception as ei:
				pass
		finally:
			self.shutdown();

	def shutdown(self):
		self.isAlive = False;
		self.device.reset();
		usb.util.dispose_resources(self.device);

	def stop(self):
		if(self.isAlive):
			self.shutdown();
			self.join();
			try:
				self.MPI.put_nowait("Stopping FX3");
			except Exception as ei:
				pass
		
	def getPipe(self):
		return self.pipeOut;


class Emulator(mp.Process):
	def __init__(self, MPI, dummyFile, bufferSize=DCS._READ_SIZE, fs=2.5E6):
		mp.Process.__init__(self);

		self.MPI = MPI;
		self.file = open(dummyFile, 'rb');
		self.bufferSize = bufferSize;
		(self.pipeOut, self.pipeIn) = mp.Pipe(duplex=False);
		self._packet = usb.util.create_buffer(self.bufferSize);

		self.loadClk = float(bufferSize)/fs;

		self.isAlive = True;

	def run(self):			
		try:
			while(self.isAlive):
				tstart = time.time();
				# self.pipeOut.send_bytes(self._dev.read(DCS._ENDPOINT_ID, self.bufferSize, DCS._TIMEOUT));
				self._packet = self.file.read(bufferSize);
				if(len(self._packet) != self.bufferSize):
					raise Exception("Device not ready");
				self.pipeOut.send_bytes(self._packet);
				trun = time.time() - tstart;

				time.sleep(max(0, self.loadClk-trun));

		except Exception as e:
			try:
				self.MPI.put_nowait(e);
			except Exception as ei:
				pass
		finally:
			self.shutdown();

	def shutdown(self):
		self.isAlive = False;
		self.file.close();

	def stop(self):
		if(self.isAlive):
			self.shutdown();
			self.join();
			try:
				self.MPI.put_nowait("Stopping FX3");
			except Exception as ei:
				pass
		
	def getPipe(self):
		return self.pipeOut;
