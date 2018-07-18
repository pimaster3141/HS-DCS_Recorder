# import code
# import DCSReader
# import BufferedWriter
# import QueuePeekerBuffer
from multiprocessing import Queue as Q
import multiprocessing as mp
# import queue
import MPWorker
# import ThreadWorker
import G2Display
import code
import time

# inBuf = None;
# outBuf = None;
# DCS = None;
# peeker = None;
# outFile = None;
# display = None;

display = None;
DCSWorker = None;
peekBuf = None;
conn1 = None;
conn2 = None;

def start(filename, sampleClk=2E6, numChannels=4, refreshRate=5, bufferDepth=20):
	# global inBuf, outBuf, peeker, DCS, outFile, display;
	global display, DCSWorker, peekBuf, conn1, conn2;

	# inBuf = queue.Queue();
	# outBuf = queue.Queue();
	peekBuf = Q();
	(conn1, conn2) = mp.Pipe()
	# DCS = DCSReader.DCSReader(inBuf);
	# peeker = QueuePeeker.QueuePeeker(inBuf, outBuf);
	# peeker = QueuePeekerBuffer.QueuePeeker(inBuf, outBuf, peekBuf);
	# outFile = BufferedWriter.BufferedWriter(outBuf, filename);
	# display = MPWorker.MPWorker(peekBuf, sampleClk, numChannels, refreshRate, bufferDepth);
	# display = ThreadWorker.ThreadWorker(peekBuf, sampleClk, numChannels, refreshRate, bufferDepth);
	
	DCSWorker = MPWorker.MPWorker(conn2, filename, peekBuf);

	DCSWorker.start();

	display = G2Display.G2GraphWindow(peekBuf, sampleClk, numChannels, refreshRate, bufferDepth)

	# outFile.start();
	# peeker.start();
	# DCS.start();

	display.run();

def stop():
	# global inBuf, outBuf, peeker, DCS, outFile, display;
	global display, DCSWorker, peekBuf, conn1, conn2;

	# DCS.shutdown();
	# peeker.shutdown();
	# outFile.shutdown();

	conn1.send('');
	print(conn1.recv());
	DCSWorker.terminate();




# start('testRun');
# time.sleep(1);
# display.run();
# print("HERE");
# import time
# time.sleep(15);
# stop();
# code.interact(local = locals());
