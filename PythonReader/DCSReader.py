import threading
import usb.core
import usb.util
import queue

import time
import numpy as np

class DCSReader(threading.Thread):

	_TIMEOUT = 1000;
	_READ_SIZE = 512000

	_VENDOR_ID = 0x04B4;
	_PRODUCT_ID = 0x00F1;
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
		del(self._dev);
		self.join();

def extractSignals(data):
	# data = np.frombuffer(data, dtype=np.int8);
	# vap = data < 0;
	# vap = np.array(vap*128, dtype = np.uint8);
	# data = data + vap;

	# data = np.diff(data);
	# e = np.array((data<0)*16, dtype=np.int8);
	# data = data + e;
	


################################################
	# data = np.frombuffer(data[::2], dtype=np.int8);
	# # vap = data < 0;
	# vap1 = np.bitwise_and(data, 0x40);
	# vap2 = np.bitwise_and(data, 0x80);

	# cn1 = np.bitwise_and(data, 0x07);
	# cn2 = np.bitwise_and(data, 0x38);
	# cn2 = np.right_shift(cn2, 3);

	# ddata = np.diff(cn1);
	# e = np.array((ddata<0)*8, dtype=np.int8);
	# cn1 = ddata + e;

	# ddata = np.diff(cn2);
	# e = np.array((ddata<0)*8, dtype=np.int8);
	# cn2 = ddata + e;



	# data = np.frombuffer(data[1::2], dtype=np.int8);
	# # vap = data < 0;
	# vap3 = np.bitwise_and(data, 0x40);
	# vap4 = np.bitwise_and(data, 0x80);

	# cn3 = np.bitwise_and(data, 0x07);
	# cn3 = np.bitwise_and(data, 0x38);
	# cn4 = np.right_shift(cn2, 3);

	# ddata = np.diff(cn3);
	# e = np.array((ddata<0)*8, dtype=np.int8);
	# cn3 = ddata + e;

	# ddata = np.diff(cn4);
	# e = np.array((ddata<0)*8, dtype=np.int8);
	# cn4 = ddata + e;

	# return(cn1,vap);
################################################




	data = np.frombuffer(data[::2], dtype=np.int8);
	vap = data < 0;

	data = np.bitwise_and(data, 0x07);
	ddata = np.diff(data);
	e = np.array((ddata<0)*8, dtype=np.int8);
	ddata = ddata + e;

	return(ddata,vap);


