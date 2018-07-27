# import code
import DCSReader
import BufferedWriter
import queue

inBuf = None;
outBuf = None;
DCS = None;
peeker = None;
outFile = None;
display = None;

def start(filename):
	global inBuf, outBuf, peeker, DCS, outFile, display;

	inBuf = queue.Queue();

	DCS = DCSReader.DCSReader(inBuf);
	outFile = BufferedWriter.BufferedWriter(inBuf, filename);
	
	outFile.start();
	DCS.start();

def stop():
	global inBuf, outBuf, peeker, DCS, outFile, display;

	DCS.shutdown();
	outFile.shutdown();




# start('testRun');
# time.sleep(1);
# display.run();
# print("HERE");
# import time
# time.sleep(15);
# stop();
# code.interact(local = locals());