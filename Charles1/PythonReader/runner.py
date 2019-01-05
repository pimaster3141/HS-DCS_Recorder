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
isDummy = False;

def start(filename, sampleClk=2E6, numChannels=4, refreshRate=5, bufferDepth=20, dummy=False, dummyData='finger'):
	# global inBuf, outBuf, peeker, DCS, outFile, display;
	global display, DCSWorker, peekBuf, conn1, conn2, isDummy;

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
	
	DCSWorker = None;

	if(not dummy):
		DCSWorker = MPWorker.MPWorker(conn2, filename, peekBuf);
		DCSWorker.start();
		isDummy=False;

	else:
		isDummy=True;

	try:
		display = G2Display.G2GraphWindow(peekBuf, sampleClk, numChannels, refreshRate, bufferDepth, dummy, dummyData)

		# outFile.start();
		# peeker.start();
		# DCS.start();

		display.run();

	except Exception as e:
		print(e);
		print("CALLING STOP");
		stop();
		
def stop():
	# global inBuf, outBuf, peeker, DCS, outFile, display;
	global display, DCSWorker, peekBuf, conn1, conn2;

	# DCS.shutdown();
	# peeker.shutdown();
	# outFile.shutdown();

	display.stop();
	conn1.send('');
	print("waiting 10s for system shutdown...");
	if(conn1.poll(10)):
		print(conn1.recv());
	else:
		print("Lost communication with DCS!");
	try:
		DCSWorker.terminate();
	except Exception as e:
		print(e);
	print("SYSTEM HALTED");


def debug(sampleClk = 2E6):
	global display, DCSWorker, peekBuf, conn1, conn2, isDummy;
	peekBuf = Q();
	(conn1, conn2) = mp.Pipe()
	
	DCSWorker = None;

	DCSWorker = MPWorker.MPWorker(conn2, None, peekBuf);
	DCSWorker.start();

	try:
		display = DebuggerDisplay.G2GraphWindow(peekBuf, sampleClk, numChannels=4, refreshRate=2, bufferDepth=10000, dummy=False, dummyData=None)

		display.run();

	except Exception as e:
		print(e);
		print("CALLING STOP");
		stop();




# start('testRun');
# time.sleep(1);
# display.run();
# print("HERE");
# import time
# time.sleep(15);
# stop();
# code.interact(local = locals());
print("Starting Up...");