from notify_run import Notify

class Pusher():
	def __init__(self, showQR=True, register=False):
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

	def send(self, message):
		self.notify.send(str(message));

