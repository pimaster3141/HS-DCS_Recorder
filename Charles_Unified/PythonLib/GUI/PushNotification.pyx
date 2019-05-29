from notify_run import Notify
from thread import start_new_thread

class Pusher():
	def __init__(self, showQR=True, register=False):
		self.notify = None;
		try:
			self.notify = Notify();
			x = None;
			if(register):
				x = self.notify.register();
			else:					
				try:
					x = self.notify.info()
				except:
					x = self.notify.register();
			if(showQR):
				print(x);
		except:
			print("Error initializing notification - skipping");
			pass;

	def send(self, message):
		if(not self.notify == None):
			try:
				# self.notify.send(str(message));
				start_new_thread(self.notify.send , (str(message)));
			except:
				print("Cannot send message - Check internet");
		

