import multiprocessing as mp
import usb.core
import usb.util
import array

class DCS(mp.Process):
	_TIMEOUT = 2000;
	_READ_SIZE = 131072;	#512KB = 524288 base2

	_ENDPOINT_ID = 0x81;

	def __init__(self, MPI, device, bufferSize = _READ_SIZE):
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
				if(len(numRead) != self.bufferSize):
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
		self.shutdown();
		self.join();
		

	def getPipe(self):
		return self.pipeOut;