import pyqtgraph as pg
import numpy as np
import time
import DCSReader
import G2Calc
import queue


class G2GraphWindow():
	def __init__(self, bufferPeek, sampleCLK=10E6, numChannels=1, refreshRate=20, bufferDepth=10):
		# mp.Process.__init__(self);

		self._peeker = bufferPeek;
		self._lastTime = time.time();

		self.win = pg.GraphicsWindow();
		self.win.setWindowTitle("G2 Display");
		
		self.g2Plot = self.win.addPlot(title = 'G2');
		self.g2Plot.setLabel('bottom',  'tau', 's');
		self.g2Plot.setLabel('left', 'G2');
		self.g2Plot.setMouseEnabled(x=False, y=False);
		self.g2Plot.enableAutoRange(x=False, y=False);
		self.g2Plot.setLogMode(x=True, y=False);
		self.g2Plot.setYRange(0.9, 1.6);
		self.win.nextRow();

		self.countPlot = self.win.addPlot(title = 'Photon Count');
		self.countPlot.setLabel('bottom', 'Time', 's');
		self.countPlot.setLabel('left', 'count', 'cps');
		self.countPlot.setLabel('right', 'count', 'cps');
		self.countPlot.setMouseEnabled(x=False, y=False);
		self.countPlot.enableAutoRange(x=True, y=True);

		self._numChannels = numChannels;
		self._refreshPeriod = 1.0/refreshRate;
		self._bufferSize = bufferDepth*refreshRate+1;
		self._sampleCLK = sampleCLK;

		self.xVals = np.linspace(-1*bufferDepth, 0, self._bufferSize);

		self.g2PlotData = [];
		self.countPlotData = [];
		self.countPlotDataAverage = [];

		self.g2Curve = [];
		self.countCurve = [];
		self.countCurveAverage = [];

		for c in range(self._numChannels):
			self.g2PlotData.append(np.array([]));
			self.countPlotData.append(np.zeros(self._bufferSize));
			self.countPlotDataAverage.append(np.zeros(self._bufferSize));
			
			self.g2Curve.append(self.g2Plot.plot(x=[1], y=[1]));
			self.countCurve.append(self.countPlot.plot(x=self.xVals, y=self.countPlotData[c]));
			self.countCurveAverage.append(self.countPlot.plot(x=self.xVals, y=self.countPlotDataAverage[c], pen='g'));


		self._timer = pg.QtCore.QTimer();
		self._retryCount = 0;
		self._isAlive = True;
		return;

	def update(self):
		# print("here");
		try:
			data = self._peeker.get(block=True, timeout=1);
			self._retryCount = 0;
			if(data == ''):
				self._isAlive = False;
				self._timer.stop();
				return;
			else:
				# data = data[::2];
				(photon, vap) = DCSReader.extractSignals(data);
				g2Data = G2Calc.mtAuto(photon, fs=self._sampleCLK, levels=16);
				count = np.mean(photon)*self._sampleCLK;
				countAverage = np.mean(self.countPlotData[0]);

				self.countPlotData[0][:-1] = self.countPlotData[0][1:]; 
				self.countPlotData[0][-1] = count;

				self.countPlotDataAverage[0][:-1] = self.countPlotDataAverage[0][1:]; 
				self.countPlotDataAverage[0][-1] = countAverage*0.8 + count*0.2;

				# print(count);
				self.countCurve[0].setData(self.xVals, self.countPlotData[0]);
				self.countCurveAverage[0].setData(self.xVals, self.countPlotDataAverage[0]);
				self.g2Curve[0].setData(g2Data[1:,0], g2Data[1:, 1]);
		except queue.Empty:
			self._retryCount = self._retryCount + 1;
			if(self._retryCount > 5):
				self._timer.stop();
			return;
		except Exception as e:
			print(e);
			self._isAlive = False;
			return;




	def run(self):
		self._timer.timeout.connect(self.update);
		self._timer.start(self._refreshPeriod*1000);

		if __name__ == '__main__':
			import sys
			if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
				QtGui.QApplication.instance().exec_()


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
