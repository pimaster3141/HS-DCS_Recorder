import threading
import usb.core
import usb.util
import queue

import time
import numpy as np

class DCSReader(threading.Thread):

	_TIMEOUT = 2000;
	_READ_SIZE = 512000

	_VENDOR_ID = 0x04B4;
	_PRODUCT_ID = 0x00F0;
	_ENDPOINT_ID = 0x81;

	def __init__(self, buffer):
		threading.Thread.__init__(self);

		self._buffer = buffer;

		self._dev = usb.core.find(idVendor=DCSReader._VENDOR_ID, idProduct=DCSReader._PRODUCT_ID);
		self._dev.set_configuration();

		self._isAlive = True;

	def run(self):
		print("Starting USB");
		self._dev.read(DCSReader._ENDPOINT_ID, 512000, DCSReader._TIMEOUT);

		while(self._isAlive):
			try:
				self._buffer.put_nowait(self._dev.read(DCSReader._ENDPOINT_ID, DCSReader._READ_SIZE, DCSReader._TIMEOUT));
			except Exception as e:
				print(e);
				print("fuck");
				print("ENDPOINT ABORTED");
				self._isAlive = False;
				continue

		print("USB CLOSED");

	def shutdown(self):
		self._isAlive = False;
		self.join();
		usb.util.dispose_resources(self._dev);
		del(self._dev);

def extractSignals(data):
	# data = np.frombuffer(data, dtype=np.int8);
	# vap = data < 0;
	# vap = np.array(vap*128, dtype = np.uint8);
	# data = data + vap;

	# data = np.diff(data);
	# e = np.array((data<0)*16, dtype=np.int8);
	# data = data + e;
	


################################################
	dataStream = np.frombuffer(data, dtype=np.int16);

	vap1 = np.bitwise_and(dataStream, 0x0001);
	vap2 = np.bitwise_and(dataStream, 0x0002);
	vap3 = np.bitwise_and(dataStream, 0x0003);
	vap4 = np.bitwise_and(dataStream, 0x0004);

	cn1 = np.bitwise_and(dataStream, 0x0070);
	cn2 = np.bitwise_and(dataStream, 0x0380);
	cn3 = np.bitwise_and(dataStream, 0x1C00);
	cn4 = np.bitwise_and(dataStream, 0xE000);

	cn1 = np.right_shift(cn1, 4);
	cn2 = np.right_shift(cn2, 7);
	cn3 = np.right_shift(cn3, 10);
	cn4 = np.right_shift(cn4, 13);

	ddata = np.diff(cn1);
	e = np.array((ddata<0)*8, dtype=np.int8);
	cn1 = ddata + e;

	ddata = np.diff(cn2);
	e = np.array((ddata<0)*8, dtype=np.int8);
	cn2 = ddata + e;

	ddata = np.diff(cn3);
	e = np.array((ddata<0)*8, dtype=np.int8);
	cn3 = ddata + e;

	ddata = np.diff(cn4);
	e = np.array((ddata<0)*8, dtype=np.int8);
	cn4 = ddata + e;

	return([cn1,cn2,cn3,cn4], [vap1,vap2,vap3,vap4]);
################################################




	# data = np.frombuffer(data[::2], dtype=np.int8);
	# vap = data < 0;

	# data = np.bitwise_and(data, 0x07);
	# ddata = np.diff(data);
	# e = np.array((ddata<0)*8, dtype=np.int8);
	# ddata = ddata + e;

	# return(ddata,vap);


