import setuptools
import pyximport; pyximport.install()

import PyQt5
import pyqtgraph as pg
import numpy as np
import DataProcessor

class GraphWindow():
	PEN_COLORS = ['w', 'y', 'g', 'b'];
	QUEUE_TIMEOUT = 5;	

	def __init__(self, processor, depth=10, legacy=False):
		self.processor = processor;
		(self.g2Source, self.flowSource) = self.processor.getBuffers();
		self.tauList = self.processor.getTauList();
		self.samplePeriod = self.processor.getTWindow();
		self.binRate = self.processor.getFs();
		self.calcFlow = self.processor.isFlowEnabled();

		self.numSamples = int((depth/self.samplePeriod)+0.5);

		self.setupDataBuffers();
		self.setupPlots(legacy);
		
	def setupPlots(self, legacy):
		self.win = None;
		if(legacy):
			self.win = pg.GraphicsWindow("Charles Sr.");
		else:
			self.win = pg.GraphicsWindow("Charles Jr.");

		self.g2Plot = self.win.addPlot(title="G2", labels={'left':('g2'),'bottom':('Delay Time', 's')}, row=0, col=0);
		self.g2Plot.setMouseEnabled(x=False, y=False);
		self.g2Plot.enableAutoRange(x=False, y=False);
		self.g2Plot.setLogMode(x=True, y=False);
		self.g2Plot.setYRange(0.9, 1.6);
		self.g2Plot.showGrid(x=True, y=True);
		self.g2Legend = self.g2Plot.addLegend();

		self.vapPlot = self.win.addPlot(title="Vaporizer", labels={'bottom':('Time', 's')}, row=0, col=1);
		self.vapPlot.setMouseEnabled(x=False, y=False);
		self.vapPlot.enableAutoRange(x=True, y=False);
		self.vapPlot.setYRange(0, 1);

		self.snrPlot = self.win.addPlot(title="SNR", labels={'left':('SNR'),'bottom':('Time', 's')}, row=1, col=0);
		self.snrPlot.setMouseEnabled(x=False, y=False);
		self.snrPlot.enableAutoRange(x=False, y=True);
		self.snrPlot.setLogMode(x=True, y=False);
		self.snrPlot.showGrid(x=False, y=True);

		self.betaPlot = self.win.addPlot(title="Beta", labels={'bottom':('Time', 's')}, row=1, col=1);
		self.betaPlot.setMouseEnabled(x=False, y=False);

		self.countPlot = self.win.addPlot(title="Photon Count", labels={'left':('Count', 'cps'),'bottom':('Time', 's')}, row=2, col=0, colspan=2);
		self.countPlot.setMouseEnabled(x=False, y=False);
		self.countPlot.enableAutoRange(x=True, y=True);

		self.flowPlot = None;
		if(self.calcFlow):
			self.flowPlot = self.win.addPlot(title="Fitted Flow", labels={'left':('aDb'), 'bottom':('Time', 's')}, row=3, col=0, colspan=2);
			self.flowPlot.setMouseEnabled(x=False, y=False);

		self.setupCurves();

	def setupCurves(self):
		self.g2Curves = [];
		self.vapCurves = [];
		self.snrCurves = [];
		self.betaCurves = [];
		self.countCurves = [];
		self.flowcurves = [];

		for c in range(self.numG2Channels):
			self.g2Curves.append(self.g2Plot.plot(x=self.tauList, y=self.g2Buffer[0,c,:], pen=GraphWindow.PEN_COLORS[c], name='CH'+str(c)));
			self.snrCurves.append(self.snrPlot.plot(x=self.tauList, y=np.mean(self.g2Buffer[:,c,:], axis=0), pen=GraphWindow.PEN_COLORS[c], name='CH'+str(c)));
			self.vapCurves.append(self.vapPlot.plot(x=self.numSamples, y=self.vapBuffer[:,c], pen=GraphWindow.PEN_COLORS[c], name='CH'+str(c)));
			self.countCurves.append(self.countPlot.plot(x=self.numSamples, y=self.countBuffer[:,c], pen=GraphWindow.PEN_COLORS[c], name='CH'+str(c)));

			if(not self.calcFlow):
				self.betaCurves.append(self.betaPlot.plot(x=self.numSamples, y=self.betaBuffer[:,c], pen=GraphWindow.PEN_COLORS[c], name='CH'+str(c)));

		if(self.calcFlow):
			pass;

	def setupDataBuffers(self):
		g2QueueData = self.g2Source.get(block=True, timeout=GraphWindow.QUEUE_TIMEOUT);
		self.numG2Channels = len(g2QueueData[0][0]);
		self.numVapChannels = len(g2QueueData[0][1]);
		
		self.g2Buffer = np.zeros((self.numSamples, self.numG2Channels, len(self.tauList)));
		self.vapBuffer = np.zeros((self.numSamples, self.numVapChannels));
		self.countBuffer = np.zeros((self.numSamples, self.numG2Channels));

		flowQueueData = None;
		self.numFlowChannels = None;
		self.flowBuffer = None;
		self.betaBuffer = None;
		if(self.calcFlow):
			data = self.flowSource.get(block=True, timeout=GraphWindow.QUEUE_TIMEOUT);

			flowData = data[:, 0];
			pass
		else:
			self.betaBuffer = np.zeros((self.numSamples, self.numG2Channels));

		self.updateDataBuffers(g2QueueData, flowQueueData);


	def updateDataBuffers(self, g2QueueData, flowQueueData):
		numShift = len(g2QueueData);
		g2Data = np.flip([item[0] for item in g2QueueData], axis=0);
		vapData = np.flip([item[1] for item in g2QueueData], axis=0);

		self.g2Buffer = np.roll(self.g2Buffer, -1*numShift, axis=0);
		self.g2Buffer[0:numShift] = g2Data;

		self.vapBuffer = np.roll(self.vapBuffer, -1*numShift, axis=0);
		self.vapBuffer[0:numShift] = vapData;

		self.countBuffer = np.roll(self.countBuffer, -1*numShift, axis=0);
		self.countBuffer[0:numShift] = self.fs/g2Data[:, :, 0];

		if(self.calcFlow):
			pass
		else:
			self.betaBuffer = np.roll(self.betaBuffer, -1*numShift);
			self.betaBuffer[0:numShift] = np.mean(g2Data[:, :, 1:4], axis=2);









