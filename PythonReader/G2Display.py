import PyQt5

import pyqtgraph as pg
import numpy as np
import time
import DCSReader
import G2Calc
import queue


class G2GraphWindow():

	penColors = ['w', 'g', 'b', 'y'];

	def __init__(self, bufferPeek, sampleCLK=2E6, numChannels=4, refreshRate=10, bufferDepth=10, dummy=False, dummyData=None):
		# mp.Process.__init__(self);
		self._numChannels = numChannels;
		self._refreshPeriod = 1.0/refreshRate;
		self._bufferSize = bufferDepth*refreshRate+1;
		self._sampleCLK = sampleCLK;

		self._peeker = bufferPeek;
		self.dummy = dummy;
		self.dummyData = None;
		self.dataPayloadSize = None;
		self.tauSize = None;

		if(self.dummy):
			self.dummyData = open(dummyData, 'rb');
			self.dataPayloadSize = int(self._sampleCLK*self._refreshPeriod);
		else:
			try:
				self.dataPayloadSize = int(len(self._peeker.get(block=True, timeout=1)));
			except Exception as e:
				print("HARDWARE ERROR");
				raise(e);
		self.tauSize = len(G2Calc.mtAuto(np.ones([int(self.dataPayloadSize/2)-1]), fs=self._sampleCLK, levels=16)[1:,0]);
		# print(self.tauSize);


		#self._lastTime = time.time();

		#SET UP WINDOW
		self.win = pg.GraphicsWindow();
		self.win.setWindowTitle("G2 Display");
		
		#SET UP PLOTS
		self.g2Plot = self.win.addPlot(title = 'G2');
		self.g2Plot.setLabel('bottom',  'tau', 's');
		self.g2Plot.setLabel('left', 'G2');
		self.g2Plot.setMouseEnabled(x=False, y=False);
		self.g2Plot.enableAutoRange(x=False, y=False);
		self.g2Plot.setLogMode(x=True, y=False);
		self.g2Plot.setYRange(0.9, 1.6);
		self.win.nextCol();

		self.countPlot = self.win.addPlot(title = 'Photon Count');
		self.countPlot.setLabel('bottom', 'Time', 's');
		self.countPlot.setLabel('left', 'count', 'cps');
		self.countPlot.setLabel('right', 'count', 'cps');
		self.countPlot.setMouseEnabled(x=False, y=False);
		self.countPlot.enableAutoRange(x=True, y=True);
		self.win.nextRow();

		self.snrPlot = self.win.addPlot(title = 'SNR');
		self.snrPlot.setLabel('bottom',  'tau', 's');
		self.snrPlot.setLabel('left', 'SNR');
		self.snrPlot.setMouseEnabled(x=False, y=False);
		self.snrPlot.enableAutoRange(x=False, y=True);
		self.snrPlot.setLogMode(x=True, y=False);
		# self.snrPlot.setYRange(0.9, 1.6);
		self.win.nextCol();

		self.vapPlot = self.win.addPlot(title = "Vaporizer");
		self.vapPlot.setLabel('bottom', 'Time', 's');
		self.vapPlot.setMouseEnabled(x=False, y=False);
		self.vapPlot.enableAutoRange(x=True, y=True);

		#SET UP CONSTANTS
		self.xVals = np.linspace(-1*bufferDepth, 0, self._bufferSize);

		#SET UP DATA STRUCTURES
		# self.g2PlotData = [];
		self.snrPlotData = [];
		self.countPlotData = [];
		self.vapPlotData = [];

		#SET UP PLOT CURVES
		self.g2Curve = [];
		self.snrCurve = [];
		self.countCurve = [];
		self.vapCurve = [];

		#LOAD INITIAL DATA
		for c in range(self._numChannels):
			# self.g2PlotData.append(np.array([]));
			self.snrPlotData.append(np.zeros([self._bufferSize, self.tauSize]));
			self.countPlotData.append(np.zeros(self._bufferSize));
			self.vapPlotData.append(np.zeros(self._bufferSize));
			
			self.g2Curve.append(self.g2Plot.plot(x=[1], y=[1], pen=G2GraphWindow.penColors[c]));
			self.snrCurve.append(self.snrPlot.plot(x=[1], y=[1], pen=G2GraphWindow.penColors[c]));
			self.countCurve.append(self.countPlot.plot(x=self.xVals, y=self.countPlotData[c], pen=G2GraphWindow.penColors[c]));
			self.vapCurve.append(self.vapPlot.plot(x=self.xVals, y=self.vapPlotData[c], pen=G2GraphWindow.penColors[c]));

		self.circularCounter=0;
		self._timer = pg.QtCore.QTimer();
		self._retryCount = 0;
		self._isAlive = True;

		self.win.closeEvent = self.closeEvent;

		return;

	def update(self):
		# print("here");

		try:

			data = None;
			if(self.dummy):
				data = self.dummyData.read(self.dataPayloadSize);

			else:
				data = self._peeker.get(block=True, timeout=1);
				self._retryCount = 0;

			if(data == '' or len(data)<self.dataPayloadSize):
				self._isAlive = False;
				self._timer.stop();
				print("NO DATA");
				return;
			else:
				# SLICE DATA
				(photon, vap) = DCSReader.extractSignals(data);

				for c in range(self._numChannels):
					# PROCESS DATA
					g2Data = G2Calc.mtAuto(photon[c], fs=self._sampleCLK, levels=16);
					# print(len(g2Data[1:,1]));
					count = np.mean(photon[c])*self._sampleCLK;
					vapData = 1*(np.sum(vap[c])>0);


					# UPDATE DATA
					self.snrPlotData[c][self.circularCounter] = g2Data[1:,1];
					self.countPlotData[c][:-1] = self.countPlotData[c][1:]; 
					self.countPlotData[c][-1] = count;
					self.vapPlotData[c][:-1] = self.vapPlotData[c][1:];
					self.vapPlotData[c][-1] = vapData;


					# UPDATE PLOTS
					self.countCurve[c].setData(self.xVals, self.countPlotData[c]);
					self.vapCurve[c].setData(self.xVals, self.vapPlotData[c]);
					self.g2Curve[c].setData(g2Data[1:,0], g2Data[1:, 1]);
					tempSNR = (np.mean(self.snrPlotData[c], 0)-1)/np.std(self.snrPlotData[c], 0);
					self.snrCurve[c].setData(g2Data[1:,0], tempSNR);

			self.circularCounter = self.circularCounter+1;
			if(self.circularCounter >= self._bufferSize):
				self.circularCounter = 0;

		except queue.Empty:
			self._retryCount = self._retryCount + 1;
			if(self._retryCount > 5):
				self._timer.stop();
			return;
		except Exception as e:
			print("im Dead");
			print(e);
			print(self.circularCounter);
			self._isAlive = False;
			self._timer.stop();
			return;




	def run(self):
		self._timer.timeout.connect(self.update);
		self._timer.start(self._refreshPeriod*1000);

		if __name__ == '__main__':
			import sys
			if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
				QtGui.QApplication.instance().exec_()

	def stop(self):
		self._timer.stop();


 
	def closeEvent(self, event):
	    print("Closing");
	    self.stop();
	    event.accept();
	    self.win.close();
	    # self.close()


 		# self.update();

 		# if(self._isAlive):
 		# 	print("IM ALIVE");
	 	# 	current = time.time();
	 	# 	deltaTime = current - self._lastTime;
	 	# 	self._lastTime = current;
	 	# 	pg.QtCore.QTimer.singleShot(max((self._refreshPeriod-deltaTime)*1000, 1), self.run);
	 	# 	print(max((self._refreshPeriod-deltaTime)*1000, 1));
	 	# else:
	 	# 	return;
