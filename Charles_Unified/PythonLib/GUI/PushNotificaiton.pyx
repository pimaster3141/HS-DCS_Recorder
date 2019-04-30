from notify_run import Notify

class Pusher():
	def __init__(self, showQR=True, register=False):
		self.notify = Notify();
		if(register):
			self.notify.register();
		if(showQR):
			self.notify.info()