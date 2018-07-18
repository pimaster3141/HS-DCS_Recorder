import threading
import queue
import time

class BufferedWriter(threading.Thread):

	def __init__(self, dataBuffer, filename):
		threading.Thread.__init__(self);

		self._buffer = dataBuffer;
		self._filename = filename;
		self._isAlive = True;

	def run(self):
		print("Starting Writer");

		if(self._filename == None):
			while(self._isAlive):
				try:
					data = self._buffer.get(block=True, timeout=1);
					# data = data[::2];
					# file.write(data);
					# file.write(self._buffer.get(block=True, timeout=1));
				except queue.Empty:
					continue;
				except Exception as e:
					print(e);
					break;

		else:
			with open('output/' + self._filename, 'wb') as file:
				while(self._isAlive):
					try:
						data = self._buffer.get(block=True, timeout=1);
					#	data = data[::2];
						file.write(data);
						# file.write(self._buffer.get(block=True, timeout=1));
					except queue.Empty:
						continue;
					except Exception as e:
						print(e);
						break;

				print("Flushing Buffer");
				count = self._buffer.qsize();
				try:
					for i in range(count):
						file.write(self._buffer.get(block=True, timeout=1));
				except queue.Empty:
					print("Error flushing buffer... aborting");

		print("Writer Closed");


	def shutdown(self):
		self._isAlive = False;
		self.join();
