import serial
import time

class Controller():
	CMD_RESET = ['reset sys'];
	CMD_INIT = ['ini la', 'ini da'];
	CMD_EN = ['en 1'];
	CMD_DIS = ['di 1'];
	CMD_LASON = ['la on'];
	CMD_LASOFF = ['la off'];
	CMD_POWER40 = ['ch 1 pow 36'];

	CHECK_RESP = str.encode('CMD> ');

	def __init__(self, port):
		self.com = None;

		try:
			self.com = serial.Serial(port = port, baudrate = 115200);
			# self.com.open();
		except:
			raise Exception('Cannot open port: ' + port);

		self.com.write(str.encode('\r\n'));
		time.sleep(1);
		if(not self.selfCheck()):
			raise Exception('Cannot detect laser');

		self.sendCommand(self.CMD_RESET);
		print("Laser Connected!");


	def selfCheck(self):
		numWaiting = self.com.inWaiting();
		if(numWaiting < 5):
			return False;

		data = self.com.read(numWaiting);
		# print(data);
		return data[-1*len(self.CHECK_RESP):] == self.CHECK_RESP;

	def sendCommand(self, commands):
		error = False;
		for command in commands:
			self.com.write(str.encode(command));
			self.com.write(str.encode('\r\n'));
			time.sleep(0.2);
			if(not self.selfCheck()):
				error = True;
		return error;

	def startLaser(self):
		print("Starting Laser");
		self.sendCommand(self.CMD_INIT);
		self.sendCommand(self.CMD_EN);
		self.sendCommand(self.CMD_POWER40);
		self.sendCommand(self.CMD_LASON);

	def stopLaser(self):
		print("Stopping Laser");
		self.sendCommand(self.CMD_LASOFF);
		self.sendCommand(self.CMD_DIS);

	def closeLaser(self):
		self.stopLaser();
		self.com.close();

