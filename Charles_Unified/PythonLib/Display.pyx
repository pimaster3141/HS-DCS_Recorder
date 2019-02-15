import setuptools
import pyximport; pyximport.install()

import PyQt5
import pyqtgraph as pg
import numpy as np
import DataProcessor

class GraphWindow():
	penColors = ['w', 'y', 'g', 'b'];
	QUEUE_TIMEOUT = 1;	

	def __init__(self, processor, detph=10, legacy=False):
		self.processor = processor;
		(self.g2Source, self.flowSource) = self.processor.getBuffers();
		self.tauList = self.processor.getTauList();
		self.samplePeriod = self.processor.getTWindow();
		self.binRate = self.processor.getFs();
		self.calcFlow = self.processor.isFlowEnabled();

		self.numSamples = int((depth/self.samplePeriod)+0.5);
		
	def setupWindow(self, legacy):
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

	def loadInitialData(self):
		data = self.g2Source.get(block=True, timeout=GraphWindow.QUEUE_TIMEOUT);

		g2Data = np.array([item[0] for item in data]);
		self.numG2Channels = len(g2Data[0]);
		
		self.g2Buffer = np.zeros((self.numSamples, self.numG2Channels, len(self.tauList)));
		self.g2Buffer[0:len(g2Data)] = g2Data;

		vapData = np.array([item[1] for item in data]);
		self.numVapChannels = len(vapData[0]);
		
		self.vapBuffer = np.zeros((self.numSamples, self.numVapChannels));
		self.vapBuffer[0:len(vapData)] = vapData;

		self.numFlowChannels = None;
		self.flowBuffer = None;
		self.betaBuffer = None;
		if(self.calcFlow):
			data = self.flowSource.get(block=True, timeout=GraphWindow.QUEUE_TIMEOUT);

			flowData = data[:, 0];
			



	def 



		flowData = None;
		if(self.calcFlow):
			flowData = self.flowSource.get(block=True, timeout=GraphWindow.QUEUE_TIMEOUT);










